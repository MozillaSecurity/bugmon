# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at http://mozilla.org/MPL/2.0/.
import logging
import os
import shutil
import subprocess
import sysconfig
import tempfile
import zipfile
from contextlib import contextmanager
from pathlib import Path, PurePosixPath
from urllib.parse import urlparse

try:
    from typing import IO, Any, Dict, Generator, Optional, TypedDict, cast
except ImportError:
    from typing import IO, Any, Dict, Generator, Optional, cast
    from typing_extensions import TypedDict

import requests
from requests.adapters import HTTPAdapter, Retry
from requests.models import Response

from bugmon.exceptions import BugmonException

HTTP_SESSION = requests.Session()
HTTP_RETRIES = Retry(total=5, read=3, connect=3, backoff_factor=1)
HTTP_SESSION.mount("http://", HTTPAdapter(max_retries=HTTP_RETRIES))
HTTP_SESSION.mount("https://", HTTPAdapter(max_retries=HTTP_RETRIES))

HG_BASE = "https://hg.mozilla.org"
MILESTONE = f"{HG_BASE}/mozilla-central/raw-file/tip/config/milestone.txt"

PERNOSCO = shutil.which("pernosco-submit")

log = logging.getLogger(__name__)


class PernoscoCreds(TypedDict):
    """Interface representing required pernosco creds"""

    PERNOSCO_USER: str
    PERNOSCO_GROUP: str
    PERNOSCO_USER_SECRET_KEY: str


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
    """Determine if revision exists for branch

    :param branch: Branch.
    :param rev: Revision.
    """
    if branch == "central":
        url = f"{HG_BASE}/mozilla-{branch}/json-rev/{rev}"
    else:
        url = f"{HG_BASE}/releases/mozilla-{branch}/json-rev/{rev}"

    return _get_url(url)


def get_source_url(branch: str, rev: str) -> str:
    """Get the source archive url

    :param branch: Source branch
    :param rev: Source revision
    """
    base = "https://hg.mozilla.org"
    if branch == "central":
        return f"{base}/mozilla-central/archive/{rev}.zip"

    return f"{base}/releases/mozilla-{branch}/{rev}.zip"


@contextmanager
def download_url(url: str) -> Generator[IO[bytes], None, None]:
    """Download a URL"""
    parsed = urlparse(url)
    ext = PurePosixPath(parsed.path).suffix

    resp = _get_url(url)
    with tempfile.TemporaryFile(suffix=ext) as temp:
        for chunk in resp.iter_content(chunk_size=128 * 1024):
            temp.write(chunk)

        temp.seek(0)
        yield temp


@contextmanager
def download_zip_archive(url: str) -> Generator[Path, None, None]:
    """Download and extract a zip archive to a temporary directory

    :param url: The url to download
    """
    with tempfile.TemporaryDirectory() as tempdir:
        with download_url(url) as file:
            with zipfile.ZipFile(file) as archive:
                archive.extractall(path=tempdir)

                yield Path(tempdir)


def is_pernosco_available() -> bool:
    """Determines if pernosco-submit is properly configured"""
    py_path = Path(sysconfig.get_path("platlib"))
    pernosco_shared = py_path / "pernoscoshared"
    return PERNOSCO is not None and pernosco_shared.exists()


def get_pernosco_trace(log_path: Path) -> Optional[Path]:
    """Identify the pernosco trace log path"""
    latest_trace = None
    for path in log_path.glob("reports/*/rr-traces/*/"):
        if path.name == "latest-trace":
            if latest_trace is not None:
                raise BugmonException("Multiple rr recordings detected!")

            latest_trace = path.resolve()

    return latest_trace


def submit_pernosco(
    trace_dir: Path,
    bug_id: int,
    creds: PernoscoCreds,
) -> None:
    """Submit pernosco trace

    :param trace_dir: Path to trace directory
    :param bug_id: Bug number
    :param creds: Pernosco credentials
    :raises BugmonException: If subprocess call fails
    """
    assert PERNOSCO is not None, "`pernosco-submit` executable not found"
    args = [
        PERNOSCO,
        "upload",
        trace_dir,
        "--title",
        bug_id,
        "--no-local-sources",
        "--consent-to-current-privacy-policy",
    ]

    try:
        subprocess.run(
            [str(arg) for arg in args],
            check=True,
            env={**os.environ, **cast(Dict[str, Any], creds)},
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        log.error("Failed to upload pernosco session: %s", e.stderr)
        raise BugmonException("Failed to upload pernosco session") from e


def has_pernosco_creds(dictionary: Dict[str, Any]) -> bool:
    """Extract Bugzilla API keys from env"""
    for name in ("PERNOSCO_USER", "PERNOSCO_GROUP", "PERNOSCO_USER_SECRET_KEY"):
        if dictionary.get(name) is None:
            log.warning(f"Cannot find Pernosco env variable {name}!")
            return False

    return True
