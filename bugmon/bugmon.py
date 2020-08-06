# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at http://mozilla.org/MPL/2.0/.

import base64
import binascii
import copy
import io
import json
import logging
import os
import platform
import re
import zipfile
from datetime import datetime as dt
from datetime import timedelta

import requests
from autobisect import EvaluatorResult
from autobisect.bisect import BisectionResult, Bisector
from autobisect.build_manager import BuildManager
from autobisect.evaluators import BrowserEvaluator, JSEvaluator
from fuzzfetch import BuildFlags, Fetcher, FetcherException
from fuzzfetch.fetch import Platform
from requests.adapters import HTTPAdapter
from urllib3 import Retry

log = logging.getLogger("bugmon")

AVAILABLE_BRANCHES = ["mozilla-central", "mozilla-beta", "mozilla-release"]

TESTCASE_URL = "https://github.com/MozillaSecurity/bugmon#testcase-identification"

HG_BASE = "https://hg.mozilla.org"
MSTONE_URL = f"{HG_BASE}/mozilla-central/raw-file/tip/config/milestone.txt"

REV_MATCH = r"([a-f0-9]{12}|[a-f0-9]{40})"
BID_MATCH = r"([0-9]{8}-)([a-f0-9]{12})"

HTTP_SESSION = requests.Session()
HTTP_ADAPTER = HTTPAdapter(max_retries=Retry(connect=3, backoff_factor=0.5))
HTTP_SESSION.mount("http://", HTTP_ADAPTER)
HTTP_SESSION.mount("https://", HTTP_ADAPTER)


def _get_url(url):
    """
    Retrieve requested URL
    """
    data = HTTP_SESSION.get(url, stream=True)
    data.raise_for_status()
    return data


def _get_milestone():
    """
    Fetch current milestone
    """
    milestone = _get_url(MSTONE_URL)
    version = milestone.text.splitlines()[-1]
    return int(version.split(".", 1)[0])


class BugException(Exception):
    """
    Exception for Bugmon related issues
    """


class ReproductionResult(object):
    """
    Class for storing reproduction results
    """

    PASSED = 0
    CRASHED = 1
    FAILED = 2
    NO_BUILD = 3

    def __init__(self, status, build_str=None):
        self.status = status
        self.build_str = build_str


class BugMonitor:
    """
    Main bugmon class
    """

    def __init__(self, bugsy, bug_num, working_dir, dry_run=False):
        """

        :param bugsy: Bugsy instance used for retrieving bugs
        :param bug_num: Bug number to analyze
        :param working_dir: Path to working directory
        :param dry_run: Boolean indicating if changes should be made to the bug
        """
        self.bugsy = bugsy
        self.bug = self.bugsy.get(bug_num, "_default")
        self.working_dir = working_dir
        self.dry_run = dry_run
        self.queue = []
        self.results = {}

        # Initialize placeholders
        self._branch = None
        self._branches = None
        self._build_flags = None
        self._comment_zero = None
        self._initial_build_id = None
        self._platform = None
        self._close_bug = False

        self.target = None
        self.evaluator = None

        self.build_manager = BuildManager()
        self.central_version = _get_milestone()

    @property
    def version(self):
        """
        Attempt to enumerate the version the bug was filed against
        """
        match = re.match(r"\d+", self.bug.version)
        if match:
            return match.group(0)

        return self.central_version

    @property
    def branch(self):
        """
        Attempt to enumerate the branch the bug was filed against
        """
        if self._branch is None:
            for alias, actual in self.branches.items():
                if self.version == actual:
                    self._branch = alias
                    break

        return self._branch

    @property
    def branches(self):
        """
        Create map of fuzzfetch branch aliases and bugzilla version tags
        :return:
        """
        if self._branches is None:
            self._branches = {
                "central": self.central_version,
                "beta": self.central_version - 1,
                "release": self.central_version - 2,
            }

            for alias in ["esr-next", "esr-stable"]:
                try:
                    rel_num = Fetcher.resolve_esr(alias)
                    if rel_num is not None:
                        self._branches[rel_num] = rel_num
                except FetcherException:
                    pass

        return self._branches

    @property
    def build_flags(self):
        """
        Attempt to enumerate build type based on flags listed in comment 0
        """
        if self._build_flags is None:
            asan = (
                "AddressSanitizer" in self.comment_zero
                or "--enable-address-sanitizer" in self.comment_zero
            )
            tsan = (
                "ThreadSanitizer" in self.comment_zero
                or "--enable-thread-sanitizer" in self.comment_zero
            )
            debug = (
                "--enable-debug" in self.comment_zero
                or "assertion" in self.bug.keywords
            )
            fuzzing = "--enable-fuzzing" in self.comment_zero
            coverage = "--enable-coverage" in self.comment_zero
            valgrind = False  # Ignore valgrind for now
            self._build_flags = BuildFlags(
                asan, tsan, debug, fuzzing, coverage, valgrind
            )

        return self._build_flags

    @property
    def comment_zero(self):
        """
        Helper function for retrieving comment zero
        """
        if self._comment_zero is None:
            comments = self.bug.get_comments()
            self._comment_zero = comments[0].text

        return self._comment_zero

    @property
    def env(self):
        """
        Attempt to enumerate any env_variables required
        """
        variables = {}
        tokens = self.comment_zero.split(" ")
        for token in tokens:
            if token.startswith("`") and token.endswith("`"):
                token = token[1:-1]
            if re.match(r"([a-z0-9_]+=[a-z0-9])", token, re.IGNORECASE):
                name, value = token.split("=")
                variables[name] = value

        return variables

    @property
    def initial_build_id(self):
        """
        Attempt to enumerate the original rev specified in comment 0 or bugmon origRev command
        """
        if self._initial_build_id is None:
            if "origRev" in self.commands and re.match(
                rf"^{REV_MATCH}$", self.commands["origRev"]
            ):
                self._initial_build_id = ["origRev"]
            else:
                for token in re.findall(r"([A-Za-z0-9_-]+)", self.comment_zero):
                    if token.startswith("`") and token.endswith("`"):
                        token = token[1:-1]

                    # Match 12 or 40 character revs
                    if re.match(rf"^{REV_MATCH}$", token, re.IGNORECASE):
                        try:
                            _get_url(f"{HG_BASE}/{self.branch}/json-rev/{token}")
                            self._initial_build_id = token
                            break
                        except requests.exceptions.HTTPError:
                            pass

                    # Match fuzzfetch build identifiers
                    if re.match(rf"^{BID_MATCH}$", token, re.IGNORECASE):
                        self._initial_build_id = token.split("-")[1]
                        break
                else:
                    # If original rev isn't specified, use the date the bug was created
                    self._initial_build_id = self.bug.creation_time.split("T")[0]

        return self._initial_build_id

    @property
    def platform(self):
        """
        Attempt to enumerate the target platform
        :return:
        """
        if self._platform is None:
            os_ = platform.system()
            if "Linux" in self.bug.op_sys:
                os_ = "Linux"
            elif "Windows" in self.bug.op_sys:
                os_ = "Windows"
            elif "Mac OS" in self.bug.op_sys:
                os_ = "Darwin"

            if os_ != platform.system():
                raise BugException("Cannot process non-native bug (%s)" % os_)

            arch = platform.machine()
            if self.bug.platform == "ARM":
                arch = "ARM64"
            elif self.bug.platform == "x86":
                arch = "i686"
            elif self.bug.platform == "x86_64":
                arch = "AMD64"

            self._platform = Platform(os_, arch)

        return self._platform

    @property
    def prefs(self):
        """
        Identify prefs in working_dir
        """
        prefs_path = None
        for filename in os.listdir(self.working_dir):
            with open(os.path.join(self.working_dir, filename)) as f:
                if filename.endswith(".js") and "user_pref" in f.read():
                    prefs_path = os.path.join(self.working_dir, filename)
        return prefs_path

    @property
    def runtime_opts(self):
        """
        Attempt to enumerate the runtime flags specified in comment 0
        """
        all_flags = JSEvaluator.get_valid_flags("tip")
        flags = []
        for flag in all_flags:
            if flag in self.comment_zero:
                match = re.search(
                    rf"(--{flag}[a-z0-9=-]*)", self.comment_zero, re.IGNORECASE
                )
                if match is not None:
                    flags.append(match.group(0))

        return flags

    @property
    def commands(self):
        """
        Attempt to extract commands from whiteboard
        """
        commands = {}
        if self.bug.whiteboard:
            match = re.search(r"(?<=\[bugmon:).[^\]]*", self.bug.whiteboard)
            if match is not None:
                for command in match.group(0).split(","):
                    if "=" in command:
                        name, value = command.split("=")
                        commands[name] = value
                    else:
                        commands[command] = None

        return commands

    @commands.setter
    def commands(self, value):
        parts = ",".join([f"{k}={v}" if v is not None else k for k, v in value.items()])
        if len(parts) != 0:
            if re.search(r"(?<=\[bugmon:)(.[^\]]*)", self.bug.whiteboard):
                if len(self.commands.keys()) != 0:
                    pattern = re.compile(r"(?<=\[bugmon:)(.[^\]]*)")
                    self.bug.whiteboard = pattern.sub(parts, self.bug.whiteboard)
                else:
                    pattern = re.compile(r"([bugmon:.[^\]]*)")
                    self.bug.whiteboard = pattern.sub("", self.bug.whiteboard)
            else:
                self.bug.whiteboard += f"[bugmon:{parts}]"
        else:
            pattern = re.compile(r"(?<=\[bugmon:)(.[^\]]*)")
            self.bug.whiteboard = pattern.sub(parts, self.bug.whiteboard)

    def add_command(self, key, value=None):
        """
        Add a bugmon command to the whiteboard
        :return:
        """
        commands = self.commands
        commands[key] = value
        self.commands = commands

    def remove_command(self, key):
        """
        Remove a bugmon command to the whiteboard
        :return:
        """
        commands = copy.copy(self.commands)
        if key in commands:
            del commands[key]

        self.commands = commands

    def fetch_attachments(self):
        """
        Download all attachments and store them in self.working_dir
        """
        testcase = None
        attachments = filter(lambda a: not a.is_obsolete, self.bug.get_attachments())
        for attachment in sorted(attachments, key=lambda a: a.creation_time):
            try:
                data = base64.decodebytes(attachment.data.encode("utf-8"))
            except binascii.Error as e:
                log.warning("Failed to decode attachment: %s", e)
                continue

            if attachment.file_name.endswith(".zip"):
                try:
                    z = zipfile.ZipFile(io.BytesIO(data))
                except zipfile.BadZipFile as e:
                    log.warning("Failed to decompress attachment: %s", e)
                    continue

                for filename in z.namelist():
                    if os.path.exists(filename):
                        log.warning("Duplicate filename identified: %s", filename)
                    z.extract(filename, self.working_dir)
                    if filename.lower().startswith("test"):
                        if testcase is not None:
                            raise BugException("Multiple testcases identified!")
                        testcase = os.path.join(self.working_dir, filename)
            else:
                dest = os.path.join(self.working_dir, attachment.file_name)
                with open(dest, "wb") as file:
                    file.write(data)
                    r = re.compile(r"^testcase.*$", re.IGNORECASE)
                    targets = [attachment.file_name, attachment.description]
                    if any(r.match(target) for target in targets):
                        if testcase is not None:
                            raise BugException("Multiple testcases identified!")
                        testcase = file.name

        return testcase

    def find_patch_rev(self, branch):
        """
        Attempt to determine patch rev for the supplied branch

        :param branch: Branch name
        :return: Patch revision
        """
        alias = f"mozilla-{branch}"
        if branch == "central":
            pattern = re.compile(rf"(?:{HG_BASE}/{alias}/rev/){REV_MATCH}")
        else:
            pattern = re.compile(rf"(?:{HG_BASE}/releases/{alias}/rev/){REV_MATCH}")

        comments = self.bug.get_comments()
        for comment in sorted(comments, key=lambda c: c.creation_time, reverse=True):
            match = pattern.match(comment.text)
            if match:
                return match.group(1)

        return None

    def needs_bisect(self):
        """
        Helper function to determine eligibility for 'bisect'
        """
        if "bisected" in self.commands:
            return False
        if "bisect" in self.commands:
            return True

        return False

    def needs_confirm(self):
        """
        Helper function to determine eligibility for 'confirm'
        """
        if "confirmed" in self.commands:
            return False
        if "confirm" in self.commands:
            return True
        if self.bug.status in ["ASSIGNED", "NEW", "UNCONFIRMED", "REOPENED"]:
            return True

        return False

    def needs_verify(self):
        """
        Helper function to determine eligibility for 'verify'
        """
        if "verified" in self.commands:
            return False
        if "verify" in self.commands:
            return True
        if self.bug.status == "RESOLVED":
            if self.bug.resolution == "FIXED":
                return True
            if self.bug.resolution in ("DUPLICATE", "INVALID", "WORKSFORME", "WONTFIX"):
                removed = re.sub(r"\[bugmon:.[^\]]*]", "", self.bug.whiteboard)
                self.bug.whiteboard = removed
                self._close_bug = True

        return False

    def bisect(self):
        """
        Attempt to enumerate the changeset that introduced or fixed the bug
        """
        tip = self.reproduce_bug(self.branch)
        if tip.status == ReproductionResult.NO_BUILD:
            log.warning("Failed to bisect bug (no build found)")
            return
        if tip.status == ReproductionResult.FAILED:
            log.warning("Failed to bisect bug (bad build)")
            return

        # If tip doesn't crash, bisect the fix
        find_fix = tip.status != ReproductionResult.CRASHED
        if find_fix:
            start = self.initial_build_id
            end = "latest"
        else:
            start = None
            end = self.initial_build_id

        bisector = Bisector(
            self.evaluator,
            self.target,
            self.branch,
            start,
            end,
            self.build_flags,
            self.platform,
            find_fix,
        )
        result = bisector.bisect()

        # Set bisected status and remove the bisect command
        self.add_command("bisected")
        if "bisect" in self.commands:
            self.remove_command("bisect")

        if result.status != BisectionResult.SUCCESS:
            output = [
                f"Failed to bisect testcase ({result.message}):",
                f"> Start: {result.start.changeset} ({result.start.id})",
                f"> End: {result.end.changeset} ({result.end.id})",
                f"> BuildFlags: {str(self.build_flags)}",
            ]
            self.report(*output)
        else:
            output = [
                f"> Start: {result.start.changeset} ({result.start.id})",
                f"> End: {result.end.changeset} ({result.end.id})",
                f"> Pushlog: {result.pushlog}",
            ]

            verb = "fixed" if find_fix else "introduced"
            self.report(
                f"The bug appears to have been {verb} in the following build range:",
                *output,
            )

    def confirm_open(self):
        """
        Attempt to confirm open test cases
        """
        tip = self.reproduce_bug(self.branch)
        if tip.status == ReproductionResult.NO_BUILD:
            log.warning("Failed to confirm bug (no build found)")
            return
        if tip.status == ReproductionResult.FAILED:
            log.warning("Failed to confirm bug (bad build)")
            return

        if tip.status == ReproductionResult.CRASHED:
            if "confirmed" not in self.commands:
                self.report(f"Verified bug as reproducible on {tip.build_str}.")
                self.bisect()
            else:
                change = dt.strptime(self.bug.last_change_time, "%Y-%m-%dT%H:%M:%SZ")
                if dt.now() - timedelta(days=30) > change:
                    self.report(f"Bug remains reproducible on {tip.build_str}")
        elif tip.status == ReproductionResult.PASSED:
            orig = self.reproduce_bug(self.branch, self.initial_build_id)
            if orig.status == ReproductionResult.CRASHED:
                log.info(f"Testcase crashes using the initial build ({orig.build_str})")
                self.bisect()
            else:
                self.report(
                    "Unable to reproduce bug using the following builds:",
                    f"> {tip.build_str}",
                    f"> {orig.build_str}",
                )

            # Remove from further analysis
            self._close_bug = True

        # Set confirmed status and remove the confirm command
        self.add_command("confirmed")
        if "confirm" in self.commands:
            self.remove_command("confirm")

    def verify_fixed(self):
        """
        Attempt to verify the bug state

        Bugs marked as resolved and fixed are verified to ensure that they are in fact, fixed
        All other bugs will be tested to determine if the bug still reproduces

        """
        if self.bug.status != "VERIFIED":
            patch_rev = self.find_patch_rev(self.branch)
            tip = self.reproduce_bug(self.branch, patch_rev)
            build_str = tip.build_str

            if tip.status == ReproductionResult.PASSED:
                initial = self.reproduce_bug(self.branch, self.initial_build_id)
                if initial.status != ReproductionResult.CRASHED:
                    self.report(
                        f"Bug appears to be fixed on {build_str} but "
                        f"BugMon was unable to reproduce using {initial.build_str}."
                    )
                else:
                    self.report(f"Verified bug as fixed on rev {build_str}.")
                    self.bug.status = "VERIFIED"

            elif tip.status == ReproductionResult.CRASHED:
                self.report(f"Bug marked as FIXED but still reproduces on {build_str}.")
                self.bug.status = "REOPENED"
                self.add_command("confirmed")

        branches_verified = True
        for alias, rel_num in self.branches.items():
            if isinstance(rel_num, int):
                flag = f"cf_status_firefox{rel_num}"
            else:
                flag = f"cf_status_firefox_{rel_num}"

            # Only check branches if bug is marked as fixed
            if getattr(self.bug, flag) == "fixed":
                patch_rev = self.find_patch_rev(alias)
                branch = self.reproduce_bug(alias, patch_rev)
                if branch.status == ReproductionResult.PASSED:
                    log.info(f"Verified fixed on {flag}")
                    setattr(self.bug, flag, "verified")
                    continue

                branches_verified = False
                if branch.status == ReproductionResult.CRASHED:
                    log.info(f"Bug remains vulnerable on {flag}")
                    setattr(self.bug, flag, "affected")

        if self.bug.status == "VERIFIED" and branches_verified:
            # Remove from further analysis
            self._close_bug = True

    def process(self):
        """
        Process bugmon commands present in whiteboard

        Available commands:
        verify - Attempt to verify the bug state
        bisect - Attempt to bisect the bug regression or, if RESOLVED, the bug fix
        """
        # Check that the branch is available on taskcluster
        if self.branch is None:
            self.report(f"Bug filed against non-supported branch ({self.version})")
            self._close_bug = True
            self.update()
            return

        # Check that we can parse the testcase
        testcase = self.fetch_attachments()
        if testcase is None:
            self.report(
                "Failed to identify testcase.  "
                "Please ensure that the testcase meets the requirements identified here: "
                "https://github.com/MozillaSecurity/bugmon#testcase-identification",
            )
            self._close_bug = True
            self.update()
            return

        # Setup the evaluators
        if self.bug.component.lower().startswith("javascript"):
            self.target = "js"
            self.evaluator = JSEvaluator(testcase, flags=self.runtime_opts)
        else:
            self.target = "firefox"
            self.evaluator = BrowserEvaluator(
                testcase, env=self.env, prefs=self.prefs, repeat=10
            )

        # Some testcases require setting the cwd to the parent dir
        previous_path = os.getcwd()
        os.chdir(self.working_dir)
        try:
            # If verify is required, don't do anything else
            if self.needs_verify():
                self.verify_fixed()
            else:
                # If confirm is required, testcase will be bisected
                if self.needs_confirm():
                    self.confirm_open()
                elif self.needs_bisect():
                    self.bisect()
        finally:
            os.chdir(previous_path)

        # Post updates and comments
        self.update()

    def reproduce_bug(self, branch, bid=None):
        """
        Method for evaluating testcase using the supplied branch and optional build ID
        Caches previous results

        :param branch: Branch where build is found
        :param bid: Build id (rev or date)
        """
        try:
            direction = Fetcher.BUILD_ORDER_ASC
            if bid is None:
                bid = "latest"
                direction = None

            build = Fetcher(
                self.target,
                branch,
                bid,
                self.build_flags,
                self.platform,
                nearest=direction,
            )
        except FetcherException as e:
            log.error(f"Error fetching build: {e}")
            return ReproductionResult(ReproductionResult.NO_BUILD)

        # Check if this branch and build was already tested
        if branch in self.results:
            if build.id in self.results[branch]:
                return self.results[branch][build.id]
        else:
            self.results[branch] = {}

        build_str = f"mozilla-{self.branch} {build.id}-{build.changeset[:12]}"
        log.info(f"Attempting to reproduce bug on {build_str}")

        with self.build_manager.get_build(build) as build_path:
            status = self.evaluator.evaluate_testcase(build_path)
            if status == EvaluatorResult.BUILD_CRASHED:
                self.results[branch][build.id] = ReproductionResult(
                    ReproductionResult.CRASHED, build_str
                )
            elif status == EvaluatorResult.BUILD_PASSED:
                self.results[branch][build.id] = ReproductionResult(
                    ReproductionResult.PASSED, build_str
                )
            else:
                self.results[branch][build.id] = ReproductionResult(
                    ReproductionResult.FAILED, build_str
                )

            return self.results[branch][build.id]

    def report(self, *messages):
        """
        Push changes or if dry_run, report to log
        :param messages: List of comments
        :return:
        """
        for message in messages:
            self.queue.append(message)
            for line in message.splitlines():
                log.info(line)

    def update(self):
        """
        Post any changes to the bug
        """
        if self._close_bug:
            if "bugmon" in self.bug.keywords:
                self.bug.keywords.remove("bugmon")
                self.report(
                    "Removing bugmon keyword as no further action possible.",
                    "Please review the bug and re-add the keyword for further analysis.",
                )

        diff = self.bug.diff()
        if diff:
            log.info(f"Changes: {json.dumps(diff)}")
            if not self.dry_run:
                self.bugsy.put(self.bug)
                self.bug.update()

        if not self.dry_run and self.queue:
            self.bug.add_comment("Bugmon Analysis:\n%s" % "\n".join(self.queue))
            self.queue = []
