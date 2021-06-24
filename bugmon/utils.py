# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at http://mozilla.org/MPL/2.0/.
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
    """
    Retrieve requested URL
    """
    data = HTTP_SESSION.get(url, stream=True)
    data.raise_for_status()
    return data


def _get_milestone() -> int:
    """
    Fetch current milestone
    """
    milestone = _get_url(MILESTONE)
    version = milestone.text.splitlines()[-1]
    return int(version.split(".", 1)[0])
