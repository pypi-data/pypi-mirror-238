"""
Absfuyu: Version [W.I.P]
---
Package versioning module

Version: 2.0.0dev1
Date updated: 30/06/2023 (dd/mm/yyyy)

Features:
- Version

Todo:
- Fix config loader
- finish version bump
"""


# Module level
###########################################################################
__all__ = [
    "__version__"
]

# Library
###########################################################################
from collections import namedtuple
import json
from pathlib import Path
import subprocess
from typing import List, Optional, Union
from urllib.error import URLError
from urllib.request import Request, urlopen

# from absfuyu import __title__
from absfuyu.core import CONFIG_PATH
from absfuyu.logger import logger
from absfuyu.util.json_method import JsonFile


# Setup - Type hint
###########################################################################
Version_ = namedtuple("Version_", ["major", "minor", "patch"])
VersionSerial = namedtuple("VersionSerial", ["major", "minor", "patch", "serial"])


# Class
###########################################################################
class ReleaseOption:
    """
    `MAJOR`, `MINOR`, `PATCH`
    """
    MAJOR: str = "major"
    MINOR: str = "minor"
    PATCH: str = "patch"

    # @staticmethod
    def all_option() -> List[str]:
        return [__class__.MAJOR, __class__.MINOR, __class__.PATCH]

class ReleaseLevel:
    """
    `FINAL`, `DEV`, `RC`
    """
    FINAL: str = "final"
    DEV: str = "dev"
    RC: str = "rc" # Release candidate

    # @staticmethod
    def all_level() -> List[str]:
        return [__class__.FINAL, __class__.DEV, __class__.RC]

class Version:
    """
    Versioning module
    """
    def __init__(
            self,
            package_name: Optional[str] = None,
            *,
            config_file_location: Union[str, Path, None] = None
        ) -> None:
        """
        package_name: Name of the package
        config_file_location: Location of the config file (.json file) if any
        """
        # Get config
        try:
            self.config_file = JsonFile(Path(config_file_location))
            cfg: dict = self.config_file.load_json()
            # version: dict = cfg.get("version", {"major": 1, "minor": 0, "patch": 0, "release_level": ReleaseLevel.FINAL, "serial": 0})
            version: dict = cfg.get("version")
        except:
            logger.error("Can't load config file")

        self.major: int = version.get("major")
        self.minor: int = version.get("minor")
        self.patch: int = version.get("patch")
        self.release_level: str = version.get("release_level")
        self.serial: int = version.get("serial")

        # Set package name
        self.package_name = package_name
    
    def __str__(self) -> str:
        temp = ".".join(map(str, self.version))
        return temp
    def __repr__(self) -> str:
        return self.__str__()
    
    @property
    def version(self) -> Union[Version_, VersionSerial]:
        """Convert into `tuple`"""
        if self.release_level.startswith(ReleaseLevel.FINAL):
            return Version_(self.major, self.minor, self.patch)
        else:
            temp = self.release_level + str(self.serial)
            return VersionSerial(self.major, self.minor, self.patch, temp)
    
    def to_dict(self) -> dict:
        """Convert into `dict`"""
        return {
            "major": self.major,
            "minor": self.minor,
            "patch": self.patch,
            "release_level": self.release_level,
            "serial": self.serial
        }
    

    # Check for update
    @staticmethod
    def _fetch_data_from_server(link: str):
        """Fetch version data of package from pypi.org"""
        req = Request(link)
        try:
            response = urlopen(req)
            # return response
        except URLError as e:
            if hasattr(e, "reason"):
                logger.error("Failed to reach server.")
                logger.error("Reason: ", e.reason)
            elif hasattr(e, "code"):
                logger.error("The server couldn\'t fulfill the request.")
                logger.error("Error code: ", e.code)
        except:
            logger.error("Fetch failed!")
        else:
            return response.read().decode()

    def _get_latest_version_legacy(self) -> str:
        """
        Load data from PyPI's RSS -- OLD
        """
        rss = f"https://pypi.org/rss/project/{self.package_name}/releases.xml"
        xml_file: str = self._fetch_data_from_server(rss)
        ver = xml_file[xml_file.find("<item>"):xml_file.find("</item>")] # First item
        version = ver[ver.find("<title>")+len("<title>"):ver.find("</title>")]
        return version

    def _load_data_from_json(self, json_link: str) -> dict:
        """
        Load data from api then convert to json
        """
        json_file: str = self._fetch_data_from_server(json_link)
        return json.loads(json_file)

    def _get_latest_version(self) -> str:
        """
        Get latest version from PyPI's API
        """
        link = f"https://pypi.org/pypi/{self.package_name}/json"
        ver: str = self._load_data_from_json(link)["info"]["version"]
        logger.debug(f"Latest: {ver}")
        return ver

    def _get_update(self):
        """
        Run pip upgrade command
        """
        cmd = f"pip install -U {self.package_name}".split()
        return subprocess.run(cmd)

    def check_for_update(
            self,
            *,
            force_update: bool = False,
        ) -> None:
        """
        Check for latest update

        force_update: Auto update the package when run
        """
        if self.package_name is None:
            logger.warning("No package name provided")
            return None
        
        try:
            latest = self._get_latest_version()
        except:
            latest = self._get_latest_version_legacy()
        current = __version__
        logger.debug(f"Current: {current} | Lastest: {latest}")
        
        if current == latest:
            print(f"You are using the latest version ({latest})")
        else:
            if force_update:
                print(f"Newer version ({latest}) available. Upgrading...")
                try:
                    self._get_update()
                except:
                    print(f"""
                    Unable to perform update.
                    Please update manually with:
                    pip install -U {self.package_name}=={latest}
                    """)
            else:
                print(f"Newer version ({latest}) available. Upgrade with:\npip install -U {self.package_name}=={latest}")


    # Bump version
    def _bump_ver(self, release_option: str):
        """
        Bumping major, minor, patch
        """
        logger.debug(f"Before: {self.version}")

        if release_option.startswith(ReleaseOption.MAJOR):
            self.major += 1
            self.minor = 0
            self.patch = 0
        elif release_option.startswith(ReleaseOption.MINOR):
            self.minor += 1
            self.patch = 0
        else:
            self.patch += 1
        
        logger.debug(f"After: {self.version}")

    def bump(
            self,
            *,
            option: str = ReleaseOption.PATCH, 
            channel: str = ReleaseLevel.FINAL
        ):
        """
        Bump current version

        option : str
            Default: "patch"
        
        channel : str
            Default: "final"
        """
        # Check conditions - use default values if fail
        if option not in ReleaseOption.all_option():
            logger.debug(ReleaseOption.all_option())
            option = ReleaseOption.PATCH
        if channel not in ReleaseLevel.all_level():
            logger.debug(ReleaseLevel.all_level())
            channel = ReleaseLevel.FINAL
        logger.debug(f"Target: {option} {channel}")
        
        # Bump ver
        if channel.startswith(ReleaseLevel.FINAL): # Final release level
            if self.release_level in [ReleaseLevel.RC, ReleaseLevel.DEV]: # current release channel is dev or rc
                self.release_level = ReleaseLevel.FINAL
                self.serial = 0
            else:
                self.serial = 0 # final channel does not need serial
                self._bump_ver(option)
        
        elif channel.startswith(ReleaseLevel.RC): # release candidate release level
            if self.release_level.startswith(ReleaseLevel.DEV): # current release channel is dev
                self.release_level = ReleaseLevel.RC
                self.serial = 0 # reset serial
            elif channel == self.release_level: # current release channel is rc
                self.serial += 1
            else: # current release channel is final
                self.release_level = channel
                self.serial = 0 # reset serial
                self._bump_ver(option)
        
        else: # dev release level
            if channel == self.release_level: # current release channel is dev
                self.serial += 1
            else: # current release channel is final or rc
                self.release_level = channel
                self.serial = 0
                self._bump_ver(option)

        # Save to __version__
        # soon
        return self.version


    def __release_to_pypi(
            self,
            option: str = ReleaseOption.PATCH,
            channel: str = ReleaseLevel.FINAL,
            safety_lock_off: bool = False,
        ) -> None:
        """
        Developer only! Not intended for end-user
        
        option: ReleaseOption
        channel: ReleaseLevel
        safety_lock_off: Set to `True` to execute this function
        """
        if not safety_lock_off:
            return None
        
        logger.debug("Bumping version...")
        
        self.bump(option=option, channel=channel)

        logger.debug(f"Version bumped. Current verion: {__version__}")
        logger.debug("Initialize building package")
        
        try:
            cmd1 = "python -m build".split()
            cmd2 = "twine upload dist/*".split()
            subprocess.run(cmd1)
            subprocess.run(cmd2)
            logger.debug("Release published!")
        except:
            logger.warning("Release failed!")
            return None


# Init
###########################################################################
__version__ = str(Version(package_name="absfuyu", config_file_location=CONFIG_PATH))
# __version__ = Version()


# Run
###########################################################################
if __name__ == "__main__":
    logger.setLevel(10)
    test = Version(package_name="absfuyu", config_file_location=CONFIG_PATH)
    print(test.version, __version__, test.__dict__)
    # print(test.bump())