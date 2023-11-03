"""Implements various functions to query and parse HTML pages from USATT website."""
from __future__ import annotations

import logging
import warnings

import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

logger = logging.getLogger(__name__)

BASEURL = "http://usatt.simplycompete.com/userAccount"
MAX_ENTRIES = 1000  # We use the maximum 1000 entries per page to minimize calls.
SUMMARY_DISPLAY_COLS = (  # Columns to get for summary.
    "First Name",
    "Last Name",
    "USATT#",
    "Location",
    "Home Club",
    "Tournament Rating",
    "Last Played Tournament",
    "League Rating",
    "Last Played League",
)


def get_ratings(usattid: int | str) -> dict:
    """
    Get ratings for a specific USATT#.

    Args:
        usattid: USATT#

    Returns: {
            "USATT#": usattid,
            "Name": " ".join(name),
            "Tournament Rating": vals[0],
            "Highest Tournament Rating": vals[1],
            "Tournaments Played": vals[2],
            "League Rating": vals[3],
            "Highest League Rating": vals[4],
            "Leagues Played": vals[5]
        }
    """
    r = requests.get(f"{BASEURL}/s2", params={"q": usattid})

    if r.status_code != 200:
        raise RuntimeError("No connection to USATT.")

    soup = BeautifulSoup(r.content, features="lxml")

    name = []

    for link in soup.find_all("a"):
        url = link.get("href")
        if "userAccount/up" in url:
            accountid = url.split("/")[-1]
            name.append(link.text)

    r = requests.get(f"{BASEURL}/up/{accountid}")
    soup = BeautifulSoup(r.content, features="lxml")
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


def get_summary(
    query: str | None = None, filter: dict | None = None, display_cols: list | tuple = SUMMARY_DISPLAY_COLS
) -> pd.DataFrame:
    """
    Get a pandas DataFrame of a summary of all USATT ratings.

    Args:
        query: Query string on USATT website. Usually a name or USATT number.
        filter: Filter criteria as a dict, e.g. {"minAge": 18}.
        display_cols: Columns to display. Defaults to everything currently shown in USATT summaries.

    Returns: Summary of USATT ratings as a Pandas DataFrame
    """
    offset = 0

    dfs = []

    params = [("displayColumns", c) for c in display_cols]
    params.append(("pageSize", MAX_ENTRIES))  # type: ignore
    params.append(("max", MAX_ENTRIES))  # type: ignore
    if query is not None:
        params.append(("q", query))
    if filter is not None:
        params.extend(filter.items())
    total_pages = -1
    url = f"{BASEURL}/s2"
    while True:
        r = requests.get(url, [*params, ("offset", offset)])

        if r.status_code != 200:
            raise RuntimeError("No connection to USATT.")

        df = pd.read_html(r.content)[0]

        if total_pages == -1:
            soup = BeautifulSoup(r.content, features="lxml")

            for link in soup.find_all("a"):
                href = link.get("href")
                if "offset" in href:
                    try:
                        total_pages = max(total_pages, int(link.text))
                    except ValueError:
                        pass
            pbar = tqdm(total=total_pages)

        pbar.update(1)

        if len(df) == 0:
            break

        logger.info(f"Entries {offset+1}-{offset+len(df)}")

        dfs.append(df)
        offset += MAX_ENTRIES
        if offset / MAX_ENTRIES > total_pages + 2:
            # In case there is a problem, we will break.
            warnings.warn(f"{offset/MAX_ENTRIES} pages detected when the total pages should be {total_pages}!")
            break

    all_data = pd.concat(dfs)
    all_data = all_data[all_data.columns[2:]]
    return all_data.set_index("USATT#")
