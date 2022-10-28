# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import copy
from pathlib import Path
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
            if "user_pref" in file.read_text():
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
        self.params["env_variables"] = evaluator.env_vars

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

        for build_flags in BrowserConfiguration.iter_build_flags(bug):
            for env_variables in BrowserConfiguration.iter_env(bug):
                for filename in BrowserConfiguration.iter_tests(working_dir):
                    if prefs and prefs == filename:
                        continue

                    for use_harness in [True, False]:
                        evaluator = BrowserEvaluator(
                            filename,
                            env=env_variables,
                            prefs=prefs,
                            repeat=10,
                            use_harness=use_harness,
                        )

                        yield cls(build_flags, evaluator)
