# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import itertools
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Iterator, Tuple

from autobisect import Evaluator
from fuzzfetch import BuildFlags

from bugmon.bug import EnhancedBug


class BugConfiguration(ABC):
    """Base configuration class"""

    ALLOWED: Tuple[str, ...] = ("*",)
    EXCLUDED: Tuple[str, ...] = ()

    def __init__(self, build_flags: BuildFlags, evaluator: Evaluator):
        """Instaniate a new instance"""
        self.build_flags = build_flags
        self.evaluator = evaluator

    @classmethod
    def iter_build_flags(cls, bug: EnhancedBug) -> Iterator[BuildFlags]:
        """Iterate over possible build flags

        :param bug: Bug instance used to detect build flags.
        """
        yield bug.build_flags

        enable_debug = "assertion" in bug.keywords and not bug.build_flags.debug
        enable_fuzzing = not bug.build_flags.fuzzing
        for debug, fuzzing in itertools.product(
            (True, False) if enable_debug else (False,),
            (True, False) if enable_fuzzing else (False,),
        ):
            if not debug and not fuzzing:
                continue

            raw_flags = bug.build_flags._asdict()
            raw_flags["debug"] = debug
            raw_flags["fuzzing"] = fuzzing
            yield BuildFlags(**raw_flags)

    @classmethod
    def iter_tests(cls, working_dir: Path) -> Iterator[Path]:
        """Iterate over possible testcases

        :param working_dir: Path to iterate over.
        """
        processed = []
        for allowed_pattern in cls.ALLOWED:
            for filename in working_dir.glob(f"{allowed_pattern}"):
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
