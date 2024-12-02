# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at http://mozilla.org/MPL/2.0/.
import abc
import base64
import binascii
import copy
import io
import json
import logging
import zipfile
from pathlib import Path
from typing import Dict, List, Optional, Union, cast

from autobisect.bisect import BisectionResult, Bisector
from autobisect.build_manager import BuildManager, BuildManagerException
from autobisect.evaluators import BrowserEvaluator, EvaluatorResult, JSEvaluator
from bugsy.bugsy import Bugsy
from fuzzfetch import BuildSearchOrder, Fetcher, FetcherException

from .bug import EnhancedBug
from .evaluator_configs import BugConfigs, BugConfiguration
from .exceptions import BugmonException
from .utils import (
    PernoscoCreds,
    get_pernosco_trace,
    is_pernosco_available,
    submit_pernosco,
)

log = logging.getLogger(__name__)

AVAILABLE_BRANCHES = ["mozilla-central", "mozilla-beta", "mozilla-release"]

TESTCASE_URL = "https://github.com/MozillaSecurity/bugmon#testcase-identification"


class ReproductionBase(metaclass=abc.ABCMeta):
    """Base reproduction result class"""


class ReproductionFailed(ReproductionBase):
    """Reproduction result representing build failures"""


class ReproductionBuildBase(ReproductionBase, metaclass=abc.ABCMeta):
    """Base reproduction class that includes build information"""

    def __init__(self, build: Fetcher) -> None:
        self.build = build
        self.build_str = f"mozilla-{build._branch} {build.id}-{build.changeset[:12]}"


class ReproductionCrashed(ReproductionBuildBase):
    """Reproduction result representing crashes"""


class ReproductionPassed(ReproductionBuildBase):
    """Reproduction result representing passes"""


class BugMonitor:
    """Main bugmon class"""

    def __init__(
        self,
        bugsy: Bugsy,
        bug: EnhancedBug,
        working_dir: Path,
        pernosco_creds: Optional[PernoscoCreds] = None,
        dry_run: Optional[bool] = False,
    ) -> None:
        """Initializes new BugMonitor instance

        :param bugsy: Bugsy instance used for retrieving bugs
        :param bug: Bug to analyze
        :param working_dir: Path to working directory
        :param pernosco_creds: Optional pernosco credentials.
        :param dry_run: Boolean indicating if changes should be made to the bug
        :raises BugmonException: If pernosco_creds is supplied but pernosco is not configured
        """
        self.bugsy = bugsy
        self.bug = bug

        self.test_dir = working_dir / "testcase"
        self.test_dir.mkdir()
        self.log_dir = working_dir / "logs"
        self.log_dir.mkdir()

        self.dry_run = dry_run
        self.pernosco_creds = pernosco_creds
        if pernosco_creds is not None and not is_pernosco_available():
            if not dry_run:
                raise BugmonException("pernosco-submit is not properly configured!")

        self.queue: List[str] = []
        self.results: Dict[str, Dict[str, ReproductionBase]] = {}
        self.build_manager = BuildManager()

        self._close_bug = False

    def _bisect(
        self, config: Optional[BugConfiguration] = None
    ) -> Union[BisectionResult, None]:
        """Attempt to enumerate the changeset that introduced or fixed the bug"""
        config = config if config is not None else self.detect_config()
        if config is None:
            return None

        tip = self._reproduce_bug(config, self.bug.branch)
        if isinstance(tip, ReproductionFailed):
            log.warning("Failed to bisect bug (bad build)")
            return None

        # If tip doesn't crash, bisect the fix
        find_fix = isinstance(tip, ReproductionPassed)
        if find_fix:
            start = self.bug.initial_build_id
            end = "latest"
        else:
            start = None
            end = self.bug.initial_build_id

        try:
            bisector = Bisector(
                config.evaluator,
                self.bug.branch,
                start,
                end,
                config.build_flags,
                self.bug.platform,
                find_fix,
            )
        except FetcherException as e:
            if "bisected" not in self.bug.commands:
                self.add_command("bisected")

            self.report(f"Unable to bisect testcase ({str(e).lower()}).")
            return None

        result = bisector.bisect()

        # Set bisected status and remove the bisect command
        if "bisected" not in self.bug.commands:
            self.add_command("bisected")
        if "bisect" in self.bug.commands:
            self.remove_command("bisect")

        if result.status != BisectionResult.SUCCESS:
            output = [
                f"Unable to bisect testcase ({result.message}):",
                f"> Start: {result.start.changeset} ({result.start.id})",
                f"> End: {result.end.changeset} ({result.end.id})",
                f"> BuildFlags: {str(config.build_flags)}\n",
            ]
            self.report(*output)
        else:
            output = [
                f"> Start: {result.start.changeset} ({result.start.id})",
                f"> End: {result.end.changeset} ({result.end.id})",
                f"> Pushlog: {result.pushlog}\n\n",
            ]

            verb = "fixed" if find_fix else "introduced"
            self.report(
                f"The bug appears to have been {verb} in the following build range:",
                *output,
            )

            # If bisection succeeds, and we're not bisecting a fix, add the regression keyword.
            if not find_fix and "regression" not in self.bug.keywords:
                self.bug.keywords.append("regression")

        return result

    def _confirm_open(self) -> None:
        """Attempt to confirm open test cases"""
        config = self.detect_config()
        if config is None:
            return None

        tip = self._reproduce_bug(config, self.bug.branch)
        if isinstance(tip, ReproductionFailed):
            log.warning("Failed to confirm bug (bad build)")
            return None

        if isinstance(tip, ReproductionCrashed):
            if "confirmed" not in self.bug.commands:
                self.report(f"Verified bug as reproducible on {tip.build_str}.")
                if "bisected" not in self.bug.commands:
                    self._bisect(config)
        elif isinstance(tip, ReproductionPassed):
            bid = self.bug.initial_build_id
            orig = self._reproduce_bug(config, self.bug.branch, bid)
            if isinstance(orig, ReproductionCrashed):
                self.report(
                    f"Testcase crashes using the initial build ({orig.build_str}) "
                    f"but not with tip ({tip.build_str}.)\n"
                )
                result = self._bisect(config)
                if result and result.status == BisectionResult.SUCCESS:
                    if self.bug.add_needinfo(self.bug.assignee["email"]):
                        nick = self.bug.assignee["nick"]
                        self.report(
                            f"{nick}, can you confirm that the above bisection range "
                            "is responsible for fixing this issue?"
                        )

            elif isinstance(orig, ReproductionPassed):
                self.report(
                    "Unable to reproduce bug using the following builds:",
                    f"> {tip.build_str}",
                    f"> {orig.build_str}",
                )

            # Remove from further analysis
            if not isinstance(orig, ReproductionFailed):
                self._close_bug = True

        # Set confirmed status and remove the confirm command
        if "confirmed" not in self.bug.commands:
            self.add_command("confirmed")
        if "confirm" in self.bug.commands:
            self.remove_command("confirm")

        return None

    def _pernosco(self) -> None:
        """Attempt to record a pernosco session"""
        if self.bug.platform.system != "Linux" or self.bug.platform.machine != "x86_64":
            self.report("Pernosco is only supported for Linux x86_64 bugs.")
            if "pernosco" in self.bug.commands:
                self.remove_command("pernosco")
            if "pernosco-wanted" in self.bug.keywords:
                self.bug.keywords.remove("pernosco-wanted")
            return None

        config = self.detect_config()
        if config is None:
            return None

        if isinstance(config.evaluator, BrowserEvaluator):
            log.info("Attempting to record a pernosco session...")

            # Update config to use no-opt
            config.build_flags.no_opt = True
            # Update evaluator settings
            config.evaluator.logs = self.log_dir
            config.evaluator.pernosco = True
            config.evaluator.repeat = 100
            config.evaluator.relaunch = 1
            config.evaluator.time_limit = 300

            result = self._reproduce_bug(
                config,
                self.bug.branch,
                self.bug.initial_build_id,
            )

            if isinstance(result, ReproductionCrashed):
                latest_trace = get_pernosco_trace(self.log_dir)
                if latest_trace is None:
                    log.error("Unable to identify a pernosco trace!")
                    return None

                branch = result.build._branch  # pylint: disable=W0212
                rev = result.build.changeset

                # Write build.json.  Only used for bugmon-tc
                build_info = latest_trace / "build.json"
                build_info.write_text(json.dumps({"branch": branch, "rev": rev}))

                log.info("Successfully recorded a pernosco session.")

                if not self.dry_run:
                    if not self.pernosco_creds:
                        log.error("Pernosco creds required for submitting traces!")
                        return None

                    log.info("Uploading pernosco session...")
                    submit_pernosco(
                        latest_trace,
                        self.bug.id,
                        self.pernosco_creds,
                    )

                self.report(
                    "Successfully recorded a pernosco session.  "
                    "A link to the pernosco session will be added here shortly."
                )
            elif isinstance(result, ReproductionPassed):
                self.add_command("pernosco-failed")
                self.report(
                    "Bugmon was unable to record a pernosco session for this bug."
                )
        elif isinstance(config.evaluator, JSEvaluator):
            self.add_command("pernosco-failed")
            self.report(
                "Pernosco sessions are currently only supported for Firefox bugs!"
            )

        if "pernosco" in self.bug.commands:
            self.remove_command("pernosco")

        if "pernosco-failed" not in self.bug.commands:
            if "pernosco-wanted" in self.bug.keywords:
                self.bug.keywords.remove("pernosco-wanted")
            self.bug.keywords.append("pernosco")

        return None

    def _verify_fixed(self) -> None:
        """Attempt to verify the bug state

        Bugs marked as resolved and fixed are verified to ensure that they are in fact,
        fixed.  All other bugs will be tested to determine if the bug still reproduces
        """
        config = self.detect_config()
        if config is None:
            return None

        if self.bug.status != "VERIFIED":
            patch_rev = self.bug.find_patch_rev(self.bug.branch)
            tip = self._reproduce_bug(config, self.bug.branch, patch_rev)

            if "verify" in self.bug.commands:
                self.remove_command("verify")

            if isinstance(tip, ReproductionPassed):
                initial = self._reproduce_bug(
                    config,
                    self.bug.branch,
                    self.bug.initial_build_id,
                )
                if isinstance(initial, ReproductionPassed):
                    self.report(
                        f"Bug appears to be fixed on {tip.build_str} but "
                        f"BugMon was unable to reproduce using {initial.build_str}."
                    )
                    self._close_bug = True
                elif isinstance(initial, ReproductionFailed):
                    self.report(
                        f"Bug appears to be fixed on {tip.build_str} but "
                        f"BugMon was unable to find a usable build for {self.bug.initial_build_id}."
                    )
                    self._close_bug = True
                else:
                    self.report(f"Verified bug as fixed on rev {tip.build_str}.")
                    if self.bug.status != "NEW":
                        self.bug.status = "VERIFIED"

            elif isinstance(tip, ReproductionCrashed):
                self.report(
                    f"Bug marked as FIXED but still reproduces on {tip.build_str}.  "
                    + "If you believe this to be incorrect, please remove the bugmon "
                    + "keyword to prevent further analysis."
                )
                self.bug.status = "REOPENED"
                if "confirmed" not in self.bug.commands:
                    self.add_command("confirmed")

        branches_verified = True
        for alias, rel_num in self.bug.branches.items():
            if isinstance(rel_num, int):
                flag = f"cf_status_firefox{rel_num}"
            else:
                flag = f"cf_status_firefox_{rel_num}"

            # Only check branches if bug is marked as fixed
            if getattr(self.bug, flag) == "fixed":
                patch_rev = self.bug.find_patch_rev(alias)
                if patch_rev is None:
                    # This may have been fixed in another bug.
                    log.warning(
                        f"Unable to find commit for fx{rel_num}.  Cannot verify fix!"
                    )
                    continue
                branch = self._reproduce_bug(config, alias, patch_rev)
                if isinstance(branch, ReproductionPassed):
                    log.info(f"Verified fixed on {flag}")
                    setattr(self.bug, flag, "verified")
                    continue

                branches_verified = False
                if isinstance(branch, ReproductionCrashed):
                    log.info(f"Bug remains vulnerable on {flag}")
                    setattr(self.bug, flag, "affected")

        if self.bug.status == "VERIFIED" and branches_verified:
            # Remove from further analysis
            self._close_bug = True

        return None

    def _reproduce_bug(
        self,
        config: BugConfiguration,
        branch: str,
        bid: Optional[str] = None,
        use_cache: Optional[bool] = True,
    ) -> ReproductionBase:
        """Reproduces the bug

        Attempts to reproduce the bug using the specified branch.  If a build id is not
        specified, tip will be used.  Supports caching previous results unless a custom
        evaluator has been supplied.

        :param config: The bug configuration to use for running the testcase
        :param branch: Branch where build is found
        :param bid: Build id (rev or date)
        :param use_cache: Check for previous result using build/bid combination
        """
        try:
            direction: Optional[BuildSearchOrder] = BuildSearchOrder.ASC
            if bid is None:
                bid = "latest"
                direction = None

            build = Fetcher(
                branch,
                bid,
                config.build_flags,
                config.evaluator.target,
                self.bug.platform,
                nearest=direction,
            )
        except FetcherException as e:
            log.error(f"Error fetching build: {e}")
            return ReproductionFailed()

        build_name = build.get_auto_name()
        # Check if this branch and build was already tested
        if branch in self.results:
            if use_cache and build_name in self.results[branch]:
                return self.results[branch][build_name]
        else:
            self.results[branch] = {}

        log.info(f"Attempting to reproduce bug on {build_name}...")

        try:
            with self.build_manager.get_build(build, config.evaluator.target) as path:
                status = config.evaluator.evaluate_testcase(path)
                result: ReproductionBase
                if status == EvaluatorResult.BUILD_CRASHED:
                    result = ReproductionCrashed(build)
                elif status == EvaluatorResult.BUILD_PASSED:
                    result = ReproductionPassed(build)
                else:
                    result = ReproductionFailed()
                self.results[branch][build_name] = result
                return self.results[branch][build_name]
        except BuildManagerException as e:
            log.error(f"Error fetching build: {e}")
            return ReproductionFailed()

    def add_command(self, key: str, value: None = None) -> None:
        """Add a bugmon command to the whiteboard

        :param key: The command key name
        :param value: The command value
        """
        commands = copy.deepcopy(self.bug.commands)
        commands[key] = value
        self.bug.commands = commands

    def remove_command(self, key: str) -> None:
        """Remove a bugmon command to the whiteboard

        :param key: The command key name
        """
        commands = copy.deepcopy(self.bug.commands)
        if key in commands:
            del commands[key]

        self.bug.commands = commands

    def fetch_attachments(self, unpack: Optional[bool] = True) -> None:
        """Download all attachments and store them in self.test_dir

        :param unpack: Boolean indicating if archives should be unpacked
        """
        attachments = filter(lambda a: not a.is_obsolete, self.bug.get_attachments())
        for attachment in sorted(attachments, key=lambda a: cast(str, a.creation_time)):
            # Ignore patches
            if attachment.content_type == "text/x-phabricator-request":
                continue

            try:
                data = base64.decodebytes(attachment.data.encode("utf-8"))
            except binascii.Error as e:
                log.warning("Failed to decode attachment: %s", e)
                continue

            if unpack and attachment.file_name.endswith(".zip"):
                try:
                    with zipfile.ZipFile(io.BytesIO(data)) as z:
                        for filename in z.namelist():
                            if (self.test_dir / filename).exists():
                                log.warning("Duplicate filename: %s", filename)
                            z.extract(filename, self.test_dir)
                except zipfile.BadZipFile as e:
                    log.warning("Failed to decompress attachment: %s", e)
                    continue

            else:
                Path(self.test_dir, attachment.file_name).write_bytes(data)

    def needs_bisect(self) -> bool:
        """Helper function to determine eligibility for 'bisect'"""
        if "bisected" in self.bug.commands:
            return False
        if "bisect" in self.bug.commands:
            return True

        return False

    def needs_confirm(self) -> bool:
        """Helper function to determine eligibility for 'confirm'"""
        confirmable = self.bug.status in ("ASSIGNED", "NEW", "UNCONFIRMED", "REOPENED")
        if confirmable and "analyze" in self.bug.commands:
            return True
        if confirmable and "confirmed" not in self.bug.commands:
            return True

        return False

    def needs_pernosco(self) -> bool:
        """Helper function to determine eligibility for 'pernosco'"""
        if "pernosco-failed" in self.bug.commands:
            return False

        return "pernosco" in self.bug.commands or "pernosco-wanted" in self.bug.keywords

    def needs_verify(self) -> bool:
        """Helper function to determine eligibility for 'verify'"""
        verifiable = self.bug.status == "RESOLVED" and self.bug.resolution == "FIXED"
        if "analyze" in self.bug.commands and verifiable:
            return True
        if verifiable and "verified" not in self.bug.commands:
            return True

        if self.bug.status == "VERIFIED":
            for rel_num in self.bug.branches.values():
                base = "cf_status_firefox"
                flag = (
                    f"{base}{rel_num}"
                    if isinstance(rel_num, int)
                    else f"{base}_{rel_num}"
                )
                if getattr(self.bug, flag) == "fixed":
                    return True

        return False

    def is_supported(self) -> bool:
        """Simple checks to determine if bug is valid candidate for Bugmon"""

        # Check that the branch is available on taskcluster
        if self.bug.branch is None:
            self.report(f"Bug filed against non-supported branch ({self.bug.version}).")
            self._close_bug = True
            return False

        if self.bug.resolution in ("DUPLICATE", "INVALID", "WORKSFORME", "WONTFIX"):
            self.report(f"No valid actions for resolution ({self.bug.resolution}).")
            self._close_bug = True
            return False

        return True

    def detect_config(self) -> Optional[BugConfiguration]:
        """Detect the evaluator configuration used to reproduce the issue"""
        bid = self.bug.initial_build_id
        branch = self.bug.branch

        build_str = None

        self.fetch_attachments()
        log.info("Attempting to identify an evaluator configuration...")
        for Config in BugConfigs:
            for config in Config.iterate(self.bug, self.test_dir):
                name = type(config).__name__
                opts = ", ".join([f"{k}: {v}" for k, v in config.params.items()])
                log.info(f"Using config: {name} ({opts})")
                result = self._reproduce_bug(config, branch, bid, False)
                if isinstance(result, ReproductionCrashed):
                    log.info("Successfully identified evaluator configuration!")
                    return config

                # Record build string for reporting failed result
                if build_str is None and isinstance(result, ReproductionBuildBase):
                    build_str = result.build_str

        if build_str is not None:
            self.report(
                f"Unable to reproduce bug {self.bug.id} using build {build_str}.  "
                + "Without a baseline, bugmon is unable to analyze this bug."
            )
        else:
            self.report("Bugmon was unable reproduce this issue.")

        self._close_bug = True
        return None

    def process(self, force_confirm: bool = False) -> None:
        """Process bugmon commands present in whiteboard

        Available commands:
        verify - Attempt to verify the bug state
        bisect - Attempt to bisect the bug regression or, if RESOLVED, the bug fix
        confirm - Attempt to confirm that testcase reproduces

        :param force_confirm: Force confirmation regardless of bug state
        """
        if not self.is_supported():
            self.commit()
            return None

        # The following actions are mutually exclusive
        if self.needs_verify():
            self._verify_fixed()
        elif self.needs_confirm():
            self._confirm_open()
        elif self.needs_bisect():
            self._bisect()
        elif force_confirm and self.bug.status in [
            "ASSIGNED",
            "NEW",
            "UNCONFIRMED",
            "REOPENED",
        ]:
            self._confirm_open()

        # Pernosco sessions can be recorded at any time
        if self.needs_pernosco():
            self._pernosco()

        # Post updates and comments
        self.commit()

        return None

    def report(self, *messages: str) -> None:
        """Output and store messages in queue
        :param messages: List of comments
        """
        for message in messages:
            self.queue.append(message)
            for line in message.splitlines():
                log.info(line)

    def commit(self) -> None:
        """Post any changes to the bug"""
        if self._close_bug:
            if "bugmon" in self.bug.keywords:
                self.bug.keywords.remove("bugmon")
                self.report(
                    "Removing bugmon keyword as no further action possible.  "
                    + "Please review the bug and re-add the keyword for further analysis."
                )

        if self.queue:
            results = "\n".join(self.queue)
            self.bug.comment = {
                "body": results,
                "is_private": False,
                "is_markdown": True,
            }
            self.queue = []

        diff = self.bug.diff()
        if diff:
            log.info(f"Changes: {json.dumps(diff)}")
            if not self.dry_run:
                self.bugsy.put(self.bug)
                self.bug.update()
