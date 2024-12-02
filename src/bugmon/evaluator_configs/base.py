# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import itertools
from abc import ABC, abstractmethod
from copy import copy
from dataclasses import fields
from pathlib import Path
from typing import Any, Dict, Iterator, Tuple, cast

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
        yielded = []
        # Ignore opt builds and non-fuzzing enabled builds
        is_opt = all(cast(bool, flag) is False for flag in fields(bug.build_flags))
        if not is_opt and bug.build_flags.fuzzing:
            yielded.append(bug.build_flags)
            yield bug.build_flags

        fuzzing = True
        for asan, debug in itertools.product([True, None], repeat=2):
            # Avoid asan-debug builds because they're not used for fuzzing
            if asan and debug:
                continue

            # Avoid opt builds
            if not asan and not debug:
                continue

            new_flags = copy(bug.build_flags)
            if asan:
                new_flags.asan = True

            if debug:
                new_flags.debug = True

            if fuzzing:
                new_flags.fuzzing = True

            if not any(flags == new_flags for flags in yielded):
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
