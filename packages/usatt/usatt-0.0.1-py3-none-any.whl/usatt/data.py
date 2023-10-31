"""Getting data from USATT website."""
from __future__ import annotations

import logging

import pandas as pd
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

BASEURL = "https://usatt.simplycompete.com/userAccount"


def get_ratings(usattid: int | str) -> dict:
    """
    Get ratings for a specific USATT#.
    :param usattid: USATT#
    :return: {
        "USATT#": usattid,
        "Name": " ".join(name),
        "Tournament Rating": vals[0],
        "Highest Tournament Rating": vals[1],
        "Tournaments Played": vals[2],
        "League Rating": vals[3],
        "Highest League Rating": vals[4],
        "Leagues Played": vals[5]
    }.
    """
    r = requests.get(f"{BASEURL}/s2", params={"q": usattid})

    if r.status_code != 200:
        raise RuntimeError("No connection to USATT.")

    soup = BeautifulSoup(r.content)

    name = []

    for link in soup.find_all("a"):
        url = link.get("href")
        if "userAccount/up" in url:
            accountid = url.split("/")[-1]
            name.append(link.text)
            break

    r = requests.get(f"http://usatt.simplycompete.com/userAccount/up/{accountid}")
    soup = BeautifulSoup(r.content)
    vals = [int(d.text) for d in soup.find_all("span", class_="details-text")]
    return {
        "USATT#": usattid,
        "Name": " ".join(name),
        "Tournament Rating": vals[0],
        "Highest Tournament Rating": vals[1],
        "Tournaments Played": vals[2],
        "League Rating": vals[3],
        "Highest League Rating": vals[4],
        "Leagues Played": vals[5],
    }


def get_usatt_summary(query: str | None = None, filter: dict | None = None) -> pd.DataFrame:
    """
    Get a pandas DataFrame of a summary of all USATT ratings.

    :param query: Query string on USATT website. Usually a name or USATT number.
    :param filter: Filter criteria as a dict, e.g. {"minAge": 18}.
    :return: Pandas DataFrame.
    """
    offset = 0

    dfs = []
    cols = [
        "First Name",
        "Last Name",
        "USATT#",
        "Location",
        "Home Club",
        "Tournament Rating",
        "Last Played Tournament",
        "League Rating",
        "Last Played League",
    ]
    params = [("displayColumns", c) for c in cols]
    params.append(("pageSize", 1000))  # type: ignore
    params.append(("max", 1000))  # type: ignore
    if query is not None:
        params.append(("q", query))
    if filter is not None:
        params.extend(filter.items())
    while True:
        url = f"{BASEURL}/s2"

        r = requests.get(url, [*params, ("offset", offset)])

        if r.status_code != 200:
            raise RuntimeError("No connection to USATT.")

        df = pd.read_html(r.content)[0]

        if len(df) == 0:
            break

        logger.info(f"Entries {offset+1}-{offset+len(df)}")

        dfs.append(df)
        offset += 1000
        if offset > 30000:
            # In case there is a problem, we will break. There shouldn't be more than 30000 USATT players.
            print("Infinite loop?")
            break

    all_data = pd.concat(dfs)
    all_data = all_data[all_data.columns[2:]]
    return all_data.set_index("USATT#")
