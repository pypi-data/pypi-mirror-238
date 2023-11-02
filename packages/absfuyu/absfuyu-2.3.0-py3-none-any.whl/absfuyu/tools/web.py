"""
Absfuyu: Web
---
Web, request, BeautifulSoup stuff

Version: 1.0.0
Date updated: 25/05/2023 (dd/mm/yyyy)
"""


# Library
###########################################################################
try:
    from bs4 import BeautifulSoup
    import requests
except ImportError:
    raise SystemExit("Please install `requests` and `bs4`")

from absfuyu.logger import logger


# Function
###########################################################################
def soup_link(link: str) -> BeautifulSoup:
    """'BeautifulSoup' the link"""
    try:
        page = requests.get(link)
        soup = BeautifulSoup(page.content, "html.parser")
        logger.debug("Soup completed!")
        return soup
    except:
        logger.error("Can't soup")
        raise SystemExit("Something wrong")


def gen_random_commit_msg():
    """Generate random commit message"""
    out = soup_link("https://whatthecommit.com/").get_text()[34:-20]
    logger.debug(out)
    return out


# Run
###########################################################################
if __name__ == "__main__":
    logger.setLevel(10)
    gen_random_commit_msg()