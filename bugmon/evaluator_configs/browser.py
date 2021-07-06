# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from pathlib import Path
from typing import Union, Generator

from autobisect import BrowserEvaluator

from .base import BaseEvaluatorConfig
from ..bug import EnhancedBug

EXTENSION_ORDER = ["html", "svg", "xml", "*"]


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


class SimpleBrowserConfig(BaseEvaluatorConfig, BrowserEvaluator):
    """Simple Browser Evaluator Configuration"""

    @classmethod
    def iterate(
        cls, bug: EnhancedBug, working_dir: Path
    ) -> Generator["SimpleBrowserConfig", None, None]:
        """Generator for iterating over possible BrowserEvaluator configurations
        :param bug: The bug to evaluate
        :param working_dir: Directory containing bug attachments
        """
        prefs = identify_prefs(working_dir)

        processed = []
        for ext in EXTENSION_ORDER:
            for filename in working_dir.glob(f"*.{ext}"):
                if filename not in processed:
                    processed.append(filename)
                else:
                    continue

                yield cls(
                    filename,
                    env=bug.env,
                    prefs=prefs,
                    repeat=10,
                    timeout=60,
                )
