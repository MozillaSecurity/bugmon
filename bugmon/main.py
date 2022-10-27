# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at http://mozilla.org/MPL/2.0/.

import argparse
import json
import logging
import os
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional, cast

from bugsy import Bugsy

from bugmon import PernoscoCreds

from .bug import EnhancedBug
from .bugmon import BugMonitor
from .exceptions import BugmonException

log = logging.getLogger("bugmon")


def parse_args(argv: Any = None) -> argparse.Namespace:
    """Arg parser

    :param argv: Command line to use instead of sys.argv (optional)
    """
    parser = argparse.ArgumentParser()
    # Optional args
    parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        help="Disable bug modification",
    )
    parser.add_argument(
        "-f",
        "--force-confirm",
        action="store_true",
        help="Force bug confirmation regardless of status",
    )

    # Bug selection
    bugs = parser.add_mutually_exclusive_group(required=True)
    bugs.add_argument("--bugs", nargs="+", help="Space separated list of bug numbers")
    bugs.add_argument(
        "-s",
        "--search",
        type=Path,
        help="Path to advanced search parameters",
    )
    args = parser.parse_args(argv)

    if args.search and not args.search.is_file():
        parser.error("Search parameter path does not exist!")

    return args


def console_init_logging() -> None:
    """Enable logging when called from console"""
    log_level = logging.INFO
    log_fmt = "[%(asctime)s] %(message)s"
    if bool(os.getenv("DEBUG")):
        log_level = logging.DEBUG
        log_fmt = "%(levelname).1s %(name)s [%(asctime)s] %(message)s"
    logging.basicConfig(format=log_fmt, datefmt="%Y-%m-%d %H:%M:%S", level=log_level)


def main(argv: Optional[Dict[str, Any]] = None) -> int:
    """Launch Bugmon

    :param argv: Command line to use instead of sys.argv (optional)
    :raises BugmonException: Re-raises any error encountered by BugMonitor
    """
    console_init_logging()
    args = parse_args(argv)

    # Get the API root, default to bugzilla.mozilla.org
    api_root = os.environ.get("BZ_API_ROOT")
    api_key = os.environ.get("BZ_API_KEY")

    if api_root is None or api_key is None:
        raise BugmonException("BZ_API_ROOT and BZ_API_KEY must be set!")

    pernosco_creds: Optional[PernoscoCreds] = None
    for name in ("PERNOSCO_USER", "PERNOSCO_GROUP", "PERNOSCO_USER_SECRET_KEY"):
        if os.environ.get(name) is None:
            log.warning(f"Cannot find Pernosco env variable {name}!")
            break
    else:
        pernosco_creds = cast(
            PernoscoCreds,
            {
                "PERNOSCO_USER": os.environ["PERNOSCO_USER"],
                "PERNOSCO_GROUP": os.environ["PERNOSCO_GROUP"],
                "PERNOSCO_USER_SECRET_KEY": os.environ["PERNOSCO_USER_SECRET_KEY"],
            },
        )

        for key in ("PERNOSCO_USER", "PERNOSCO_GROUP", "PERNOSCO_USER_SECRET_KEY"):
            os.environ.pop(key)

    bugsy = Bugsy(api_key=api_key, bugzilla_url=api_root)

    if args.bugs:
        bug_list = ",".join(args.bugs)
        params = {"id": bug_list}
    else:
        params = json.loads(args.search.read_text())
        params["include_fields"] = "_default"

    response = bugsy.request("bug", params=params)
    bugs = [EnhancedBug(bugsy, **bug) for bug in response["bugs"]]

    for bug in bugs:
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                working_dir = Path(temp_dir)
                bugmon = BugMonitor(
                    bugsy,
                    bug,
                    working_dir,
                    pernosco_creds,
                    args.dry_run,
                )
                log.info(
                    f"Analyzing bug {bug.id} "
                    f"(Status: {bugmon.bug.status}, "
                    f"Resolution: {bugmon.bug.resolution})"
                )
                bugmon.process(args.force_confirm)
            except BugmonException as e:
                log.error(f"Error processing bug {bug.id}: {e}")
                return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
