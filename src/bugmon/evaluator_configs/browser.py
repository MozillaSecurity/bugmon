# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import copy
from itertools import product
from pathlib import Path
from platform import system
from typing import Dict, Iterator, Union

from autobisect import BrowserEvaluator
from fuzzfetch import BuildFlags

from ..bug import EnhancedBug
from .base import BugConfiguration


def identify_prefs(attachment_dir: Path) -> Union[Path, None]:
    """Determine if the bug includes a prefs.js file

    :param attachment_dir: Path to the downloaded attachments
    :return:
    """
    prefs_path = None
    for file in attachment_dir.rglob("*"):
        if file.suffix == ".js":
            if "user_pref" in file.read_text(encoding="utf-8"):
                prefs_path = file

    return prefs_path


class BrowserConfiguration(BugConfiguration):
    """Simple Browser Evaluator Configuration"""

    ALLOWED = ("*.htm", "*.html", "*.svg", "*.xml", "*")
    EXCLUDED = ("*.js", "*.txt")

    def __init__(self, build_flags: BuildFlags, evaluator: BrowserEvaluator):
        super().__init__(build_flags, evaluator)
        self.params["entry_point"] = evaluator.testcase
        self.params["use_harness"] = evaluator.use_harness
        self.params["use_prefs"] = bool(evaluator.prefs)
        self.params["env_variables"] = evaluator.env_vars

    @classmethod
    def iter_tests(cls, working_dir: Path) -> Iterator[Path]:
        """Iterate over possible testcases.

        :param working_dir: Path to iterate over.
        """
        testcases = list(super().iter_tests(working_dir))
        for i, path in enumerate(testcases):
            # If test_info exists, prefer it and use the parent directory
            if path.name == "test_info.json":
                new_path = testcases.pop(i).parent
                testcases.insert(0, new_path)
                break

        yield from testcases

    @staticmethod
    def iter_env(bug: EnhancedBug) -> Iterator[Dict[str, str]]:
        """Iterate over possible env variable settings

        :param bug: Bug instance used to detect env variables
        """
        yield bug.env

        if (
            bug.component == "Disability Access APIs"
            and "GNOME_ACCESSIBILITY" not in bug.env
        ):
            env_variables = copy.deepcopy(bug.env)
            env_variables["GNOME_ACCESSIBILITY"] = "1"
            yield env_variables

    @classmethod
    def iterate(
        cls, bug: EnhancedBug, working_dir: Path
    ) -> Iterator["BrowserConfiguration"]:
        """Generator for iterating over possible BrowserEvaluator configurations

        :param bug: The bug to evaluate
        :param working_dir: Directory containing bug attachments
        """
        prefs = identify_prefs(working_dir)

        for build_flags, env_variables, testcase in product(
            BrowserConfiguration.iter_build_flags(bug),
            BrowserConfiguration.iter_env(bug),
            BrowserConfiguration.iter_tests(working_dir),
        ):
            if prefs and prefs == testcase:
                continue

            for use_harness in [True, False]:
                # Don't always use prefs if they exist as they might be invalid
                for pref_path in [prefs, None] if prefs is not None else [None]:
                    evaluator = BrowserEvaluator(
                        testcase,
                        env=env_variables,
                        display="default" if system() == "Windows" else "xvfb",
                        prefs=pref_path,
                        repeat=10,
                        relaunch=1,
                        use_harness=use_harness,
                    )

                    yield cls(build_flags, evaluator)
