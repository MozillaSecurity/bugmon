# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at http://mozilla.org/MPL/2.0/.
from pathlib import Path
from typing import Union

import requests
from requests.adapters import HTTPAdapter, Retry
from requests.models import Response

HTTP_SESSION = requests.Session()
HTTP_ADAPTER = HTTPAdapter(max_retries=Retry(connect=3, backoff_factor=0.5))
HTTP_SESSION.mount("http://", HTTP_ADAPTER)
HTTP_SESSION.mount("https://", HTTP_ADAPTER)

HG_BASE = "https://hg.mozilla.org"
MILESTONE = f"{HG_BASE}/mozilla-central/raw-file/tip/config/milestone.txt"


def _get_url(url: str) -> Response:
    """Retrieve requested URL"""
    data = HTTP_SESSION.get(url, stream=True)
    data.raise_for_status()
    return data


def _get_milestone() -> int:
    """Fetch current milestone"""
    milestone = _get_url(MILESTONE)
    version = milestone.text.splitlines()[-1]
    return int(version.split(".", 1)[0])


def _get_rev(branch: str, rev: str) -> Response:
    """Determine if revision exists for branch"""
    if branch == "central":
        url = f"{HG_BASE}/mozilla-{branch}/json-rev/{rev}"
    else:
        url = f"{HG_BASE}/releases/mozilla-{branch}/json-rev/{rev}"

    return _get_url(url)


def find_pernosco_trace_dir(parent_dir: Path) -> Union[Path, None]:
    """Identify path to pernosco trace directory.

    :param parent_dir: Parent directory path.
    """
    matches = list((parent_dir / "reports").glob("**/rr-traces/"))
    if len(matches) == 1:
        return matches[0]

    return None
