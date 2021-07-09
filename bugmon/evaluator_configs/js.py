# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from pathlib import Path
from typing import Iterator

from autobisect import JSEvaluator

from .base import BaseEvaluatorConfig
from ..bug import EnhancedBug

ALLOWED = ["*.js", "*"]


class SimpleJSConfig(BaseEvaluatorConfig, JSEvaluator):
    """Simple Browser Evaluator Configuration"""

    @classmethod
    def iterate(cls, bug: EnhancedBug, working_dir: Path) -> Iterator["SimpleJSConfig"]:
        """Generator for iterating over possible JSEvaluator configurations

        Iterates over file attachments to determine the correct entry-point.

        :param bug: The bug to evaluate
        :param working_dir: Directory containing bug attachments
        """
        processed = []
        for allowed_pattern in ALLOWED:
            for filename in working_dir.glob(f"{allowed_pattern}"):
                if filename in processed:
                    continue

                processed.append(filename)
                yield cls(
                    filename,
                    flags=bug.runtime_opts,
                    repeat=10,
                    timeout=60,
                )
