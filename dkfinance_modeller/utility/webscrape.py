import multiprocessing as mp
import re
import urllib.request
from typing import Dict, List


def justetf_info(ISIN: str) -> Dict[str, object]:
    """
    Få information omkring given ETF fra justetf.com/en/.

    Args:
      ISIN: ISIN for ETFen.

    Returns:
      En dict med fundne information om ETFen.
    """
    info = {"isin": ISIN, "succes": True}
    try:
        url = (
            f"https://www.justetf.com/en/etf-profile.html"
            f"?query={ISIN}&groupField=index&from=search&isin={ISIN}#overview"
        )
        page = urllib.request.urlopen(url)
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")
        # Find replication
        idx = html.find("Replication")
        html_slice = html[idx : idx + 500]
        part1 = re.search('<span class="val">(.*?)</span>', html_slice)
        part2 = re.search('<span class="val2">(.*?)</span>', html_slice)
        if part1 is not None and part2 is not None:
            info["replication"] = f"{part1.group(1)} ({part2.group(1)})"
        else:
            raise Exception
        # Find ÅOP
        idx = html.find("Total expense ratio")
        html_slice = html[idx - 200 : idx]
        part = re.search('<div class="val">(.*?)</div>', html_slice)
        if part is not None:
            info["åop"] = part.group(1).strip("% p.a.")
        else:
            raise Exception
        # Find indeks
        idx = html.find("Investment strategy")
        html_slice = html[idx : idx + 500]
        # Check for "The"
        part = re.search("<p>The(.*?)tracks", html_slice)
        if part is None:
            # Check for "Der"
            part = re.search("<p>Der(.*?)tracks", html_slice)
        if part is not None:
            info["indeks"] = part.group(1)[1:-1].replace("&amp;", "&")
        else:
            info["indeks"] = "Intet indeks fundet"
        # Find navn
        navn_tracker = re.search("title>(.*?)</title>", html)
        if navn_tracker is not None:
            info["navn"] = navn_tracker.group(1).split("|")[0][0:-1].replace("&amp;", "&")
        else:
            raise Exception
        # Find domicile
        idx = html.find("Fund domicile")
        html_slice = html[idx : idx + 500]
        part = re.search('<td class="val">(.*?)</td>', html_slice)
        if part is not None:
            info["domicile"] = part.group(1)
        else:
            raise Exception
    except:  # noqa: E722 # pylint: disable=W0702
        info["succes"] = False
    return info


def få_etf_info(ISINer: List[str], threads: int) -> List[Dict[str, object]]:
    """
    Få information omkring givne ETFer fra justetf.com/en/.

    Args:
      ISIN: Liste af ISINer for ETFer.

    Returns:
      En liste af dicts med fundne information om ETFen.
    """
    pool = mp.Pool(threads)
    resultater = pool.map(justetf_info, ISINer)
    pool.close()
    pool.join()
    return resultater
