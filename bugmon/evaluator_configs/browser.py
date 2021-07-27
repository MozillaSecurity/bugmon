# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import copy
from pathlib import Path
from typing import Union, Iterator, Dict

from autobisect import BrowserEvaluator

from .base import BugConfiguration
from ..bug import EnhancedBug


def identify_prefs(attachment_dir: Path) -> Union[Path, None]:
    """Determine if the bug includes a prefs.js file

    :param attachment_dir: Path to the downloaded attachments
    :return:
    """
    prefs_path = None
    for file_name in attachment_dir.iterdir():
        if file_name.suffix == ".js":
            file_path = Path(attachment_dir / file_name)
            if "user_pref" in file_path.read_text():
                prefs_path = file_path

    return prefs_path


class BrowserConfiguration(BugConfiguration):
    """Simple Browser Evaluator Configuration"""

    ALLOWED = ("*.htm", "*.html", "*.svg", "*.xml", "*")
    EXCLUDED = ("*.js", "*.txt")

    @staticmethod
    def iter_env(bug: EnhancedBug) -> Iterator[Dict[str, str]]:
        """Iterate over possible env variable settings

        :param bug: Bug instance used to detect env variables
        """
        yield bug.env

        if bug.component == "Accessibility" and "GNOME_ACCESSIBILITY" not in bug.env:
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
                    evaluator = BrowserEvaluator(
                        filename,
                        env=env_variables,
                        prefs=prefs,
                        repeat=1,
                        timeout=30,
                    )

                    yield cls(build_flags, evaluator)
