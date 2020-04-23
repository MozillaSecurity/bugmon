import argparse
import json
import logging
import os
import sys
import tempfile

from bugsy import Bug, Bugsy

from bugmon import BugMonitor, BugException

log = logging.getLogger("bugmon")


def parse_args(argv=None):
    """
    Arg parser

    :param argv: Command line to use instead of sys.argv (optional)
    """
    parser = argparse.ArgumentParser()

    # Optional args
    parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        help="If enabled, don't make any remote changes",
    )

    # Bug selection
    bug_list = parser.add_mutually_exclusive_group(required=True)
    bug_list.add_argument(
        "--bugs", nargs="+", help="Space separated list of bug numbers"
    )
    bug_list.add_argument(
        "-s", "--search-params", help="Path to advanced search parameters"
    )
    args = parser.parse_args(argv)

    if args.search_params and not os.path.isfile(args.search_params):
        raise parser.error("Search parameter path does not exist!")

    return args


def console_init_logging():
    """
    Enable logging when called from console
    """
    log_level = logging.INFO
    log_fmt = "[%(asctime)s] %(message)s"
    if bool(os.getenv("DEBUG")):
        log_level = logging.DEBUG
        log_fmt = "%(levelname).1s %(name)s [%(asctime)s] %(message)s"
    logging.basicConfig(format=log_fmt, datefmt="%Y-%m-%d %H:%M:%S", level=log_level)


def main(argv=None):
    """
    Launch Bugmon

    :param argv: Command line to use instead of sys.argv (optional)
    :return:
    """
    console_init_logging()
    args = parse_args(argv)

    # Get the API root, default to bugzilla.mozilla.org
    api_root = os.environ.get("BZ_API_ROOT")
    api_key = os.environ.get("BZ_API_KEY")

    if api_root is None or api_key is None:
        raise BugException("BZ_API_ROOT and BZ_API_KEY must be set!")

    bugsy = Bugsy(api_key=api_key, bugzilla_url=api_root)

    bug_ids = []
    if args.bugs:
        bug_ids.extend(args.bugs)
    else:
        with open(args.search_params) as f:
            params = json.load(f)
            response = bugsy.request("bug", params=params)
            bugs = [Bug(bugsy, **bug) for bug in response["bugs"]]
            bug_ids.extend(sorted([bug.id for bug in bugs]))

    for bug_id in bug_ids:
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                bugmon = BugMonitor(bugsy, bug_id, temp_dir, args.dry_run)
                log.info(
                    f"Analyzing bug {bug_id} (Status: {bugmon.bug.status}, Resolution: {bugmon.bug.resolution})"
                )
                bugmon.process()
            except BugException as e:
                log.error(f"Error processing bug {bug_id}: {e}")


if __name__ == "__main__":
    sys.exit(main())
