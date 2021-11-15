# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from pathlib import Path
from typing import Iterator

from autobisect import JSEvaluator
from fuzzfetch import BuildFlags

from .base import BugConfiguration
from ..bug import EnhancedBug


class JSConfiguration(BugConfiguration):
    """Simple Browser Evaluator Configuration"""

    ALLOWED = ("*.js", "*")

    def __init__(self, build_flags: BuildFlags, evaluator: JSEvaluator):
        super().__init__(build_flags, evaluator)
        self.params["entry_point"] = str(evaluator.testcase)
        self.params["run_flags"] = evaluator.flags

    @classmethod
    def iterate(
        cls, bug: EnhancedBug, working_dir: Path
    ) -> Iterator["JSConfiguration"]:
        """Generator for iterating over possible JSEvaluator configurations

        Iterates over file attachments to determine the correct entry-point.

        :param bug: The bug to evaluate
        :param working_dir: Directory containing bug attachments
        """
        for build_flags in JSConfiguration.iter_build_flags(bug):
            for filename in JSConfiguration.iter_tests(working_dir):
                evaluator = JSEvaluator(
                    filename,
                    flags=bug.runtime_opts,
                    repeat=10,
                    timeout=60,
                )

                yield cls(build_flags, evaluator)
