# -*- coding: utf-8 -*-
"""
Automatically short link on rebrand.ly
"""


# Library
##############################################################
import json as __json
import os as __os

try:
    import requests as __requests
except ImportError:
    from absfuyu.config import show_cfg as __aie
    if __aie("auto-install-extra", raw=True):
        __cmd: str = "python -m pip install -U absfuyu[tools]".split()
        from subprocess import run as __run
        __run(__cmd)
    else:
        raise SystemExit("This feature is in absfuyu[tools] package")


# Define
##############################################################
__here = __os.path.abspath(__os.path.dirname(__file__))
__config_name = "rebrandly-api"
__config_template = """\
{
    "api": null,
    "workspace": null,
    "loaded": true
}
"""



# Config stuff
##############################################################
def __load_cfg(config_name: str = __config_name):
    """Load configuration file"""
    with open(f"{__here}/{config_name}.json") as json_cfg:
        cfg = __json.load(json_cfg)
    return cfg

def __save_cfg(config, config_name: str = __config_name):
    """Save config"""
    cfg = __json.dumps(config, indent=4, sort_keys=True)
    with open(f"{__here}/{config_name}.json","w") as json_cfg:
        json_cfg.writelines(cfg)
    return None

def __init_cfg(config_name: str = __config_name, force: bool = False):
    """Make new config when config file does not exist"""
    if __os.path.isfile(f"{config_name}.json"):
        return None
    else:
        cfg = __json.loads(__config_template)
        __save_cfg(cfg, config_name=config_name)
    if force:
        cfg = __json.loads(__config_template)
        __save_cfg(cfg, config_name=config_name)

def reset_cfg():
    """Reset config to default value"""
    __init_cfg(force=True)
    pass



# API stuff
##############################################################
def get_api(api: str = None, workspace: str = None):
    """Get API"""
    data = __load_cfg()

    # API
    if data["api"] is None:
        if api is None:
            key = input("Enter API: ")
            data["api"] = key
        else:
            data["api"] = api
    else:
        if api is None:
            pass
        else:
            if data["api"] == api:
                pass
            else:
                data["api"] = api

    # Workspace
    if data["workspace"] is None:
        if api is None:
            key = input("Enter workspace ID: ")
            data["workspace"] = key
        else:
            data["workspace"] = api
    else:
        if api is None:
            pass
        else:
            if data["workspace"] == api:
                pass
            else:
                data["workspace"] = api

    __save_cfg(data)
    return data


# Short link
##############################################################
def short_link(
        destination: str = None,
        slash_tag: str = None,
        title: str = None,
        domain: dict = None,
        api: str = None,
        workspace: str = None,
        no_trace: bool = False,
    ):
    """
    Short link using Rebrand.ly API

    Parameters:
    ---
    destination : str
        URL (start with http/https)
    
    slash_tag : str
        Custom shortlink name
    
    title : str
        Title of link
    
    domain : dict
        Domain
        [Default: rebrand.ly]
    
    api : str
        User's API
    
    workspace : str
        User's Workspace ID
    
    no_trace : bool
        Reset API every run
        [Default: False]
    """

    linkRequest = {}

    if destination is None:
        destination = input("Enter link: ")

    linkRequest["destination"] = destination
    linkRequest["domain"] = { "fullName": "rebrand.ly" }
   
    if domain is not None:
        linkRequest["domain"] = domain
    
    if slash_tag is not None:
        linkRequest["slashtag"] = slash_tag
    
    if title is not None:
        linkRequest["title"] = title
    

    get_api(api, workspace)
    api_stuff = __load_cfg()
    requestHeaders = {
        "Content-type": "application/json",
        "apikey": api_stuff["api"],
        "workspace": api_stuff["workspace"]
    }

    r = __requests.post("https://api.rebrandly.com/v1/links", 
        data = __json.dumps(linkRequest),
        headers=requestHeaders)

    
    if (r.status_code == __requests.codes.ok):
        link = r.json()
        print(f"Long URL was {link['destination']}, short URL is {link['shortUrl']}")
        # return link['shortUrl']
    else:
        raise SystemExit("FAILED!")
    
    if no_trace:
        reset_cfg()
    
    return link['shortUrl']
    


# Run
##############################################################
try:
    __Load = __load_cfg()
    if not __Load["loaded"]:
        raise SystemExit("Unable to load")
except:
    __init_cfg()