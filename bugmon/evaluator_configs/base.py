# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import itertools
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Iterator, Tuple

from autobisect import Evaluator
from fuzzfetch import BuildFlags

from bugmon.bug import EnhancedBug


class BugConfiguration(ABC):
    """Base configuration class"""

    params: Dict[str, Any]

    ALLOWED: Tuple[str, ...] = ("*",)
    EXCLUDED: Tuple[str, ...] = ()

    def __init__(self, build_flags: BuildFlags, evaluator: Evaluator):
        """Instaniate a new instance"""
        self.build_flags = build_flags
        self.evaluator = evaluator
        self.params = {"flags": build_flags.build_string()[1:]}

    @classmethod
    def iter_build_flags(cls, bug: EnhancedBug) -> Iterator[BuildFlags]:
        """Iterate over possible build flags

        :param bug: Bug instance used to detect build flags.
        """
        # Don't yield and empty build flags object
        if not all(flag is False for flag in bug.build_flags):
            yield bug.build_flags

        for asan, debug, fuzzing in itertools.product(
            (True, None) if not bug.build_flags.asan else (None,),
            (True, None) if not bug.build_flags.debug else (None,),
            (True, None) if not bug.build_flags.fuzzing else (None,),
        ):
            # Don't yield and empty build flags object
            if all(flag is None for flag in [asan, debug, fuzzing]):
                continue

            # Avoid asan-debug builds because they're not used for fuzzing
            if asan is True and debug is True:
                continue

            raw_flags = bug.build_flags._asdict()
            if asan is not None:
                raw_flags["asan"] = asan

            if debug is not None:
                raw_flags["debug"] = debug

            if fuzzing is not None:
                raw_flags["fuzzing"] = fuzzing

            new_flags = BuildFlags(**raw_flags)
            if new_flags != bug.build_flags:
                yield new_flags

    @classmethod
    def iter_tests(cls, working_dir: Path) -> Iterator[Path]:
        """Iterate over possible testcases

        :param working_dir: Path to iterate over.
        """
        processed = []
        for allowed_pattern in cls.ALLOWED:
            for filename in working_dir.rglob(f"{allowed_pattern}"):
                if not filename.is_file():
                    continue

                is_excluded = False
                for excluded_pattern in cls.EXCLUDED:
                    if filename.match(excluded_pattern):
                        is_excluded = True
                        break

                if is_excluded or filename in processed:
                    continue

                processed.append(filename)
                yield filename

    @classmethod
    @abstractmethod
    def iterate(
        cls, bug: EnhancedBug, working_dir: Path
    ) -> Iterator["BugConfiguration"]:
        """Generator for iterating over possible Evaluator configurations
        :param bug: The bug to evaluate
        :param working_dir: Directory containing bug attachments
        :return: Class instance
        """
