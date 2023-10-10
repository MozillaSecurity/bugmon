# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at http://mozilla.org/MPL/2.0/.
import copy
import tempfile
from pathlib import Path

from fuzzfetch import BuildFlags

from bugmon.bug import EnhancedBug
from bugmon.evaluator_configs import (
    BrowserConfiguration,
    BugConfiguration,
    JSConfiguration,
)


def test_bug_configuration_iter_build_flags_001(bug_data):
    """Test BugConfiguration.iter_build_flags() with assertion keyword"""
    bug = copy.deepcopy(bug_data)
    bug["keywords"] = ["assertion"]
    bug["comments"][0]["text"] = ""
    bug = EnhancedBug(None, **bug)
    build_flags = list(BugConfiguration.iter_build_flags(bug))

    # Check for the expected number of flag combinations
    assert len(build_flags) == 2
    # Check that all results are BuildFlags
    assert all(isinstance(x, BuildFlags) for x in build_flags)
    # Check for duplicates
    assert len(build_flags) == len(set(build_flags))


def test_bug_configuration_iter_build_flags_002(bug_data):
    """Test BugConfiguration.iter_build_flags() with fuzzing already enabled"""
    bug = copy.deepcopy(bug_data)
    bug["comments"][0]["text"] = "--enable-fuzzing"
    bug = EnhancedBug(None, **bug)
    build_flags = list(BugConfiguration.iter_build_flags(bug))

    # Check for the expected number of flag combinations
    assert len(build_flags) == 3
    # Check that all results are BuildFlags
    assert all(isinstance(x, BuildFlags) for x in build_flags)
    # Check for duplicates
    assert len(build_flags) == len(set(build_flags))


def test_bug_configuration_iter_tests_001():
    """Simple test of BugConfiguration.iter_tests()"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        for n in range(10):
            Path(tmp_path / f"{n}.html").touch()

        tests = list(BugConfiguration.iter_tests(tmp_path))
        assert len(tests) == 10
        assert all(isinstance(x, Path) for x in tests)


def test_browser_configuration_iter_tests_001():
    """Test BrowserConfiguration.iter_tests() with excluded list"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        Path(tmp_path / "1.html").touch()
        Path(tmp_path / "2.xml").touch()
        Path(tmp_path / "3.js").touch()

        tests = list(BrowserConfiguration.iter_tests(tmp_path))
        assert len(tests) == 2
        assert Path(tmp_path / "1.html") in tests
        assert Path(tmp_path / "2.xml") in tests


def test_browser_configuration_env_iter_001(bug_data):
    """Test BugConfiguration.env_iter() with Accessibility component"""
    bug = copy.deepcopy(bug_data)
    bug["component"] = "Disability Access APIs"
    bug = EnhancedBug(None, **bug)
    env_vars = list(BrowserConfiguration.iter_env(bug))

    assert len(env_vars) == 2
    assert "GNOME_ACCESSIBILITY" in env_vars[1]
    assert env_vars[1]["GNOME_ACCESSIBILITY"] == "1"


def test_browser_configuration_iterate_001(bug_data):
    """Simple test BrowserConfiguration.iterate()"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        Path(tmp_path / "1.html").touch()
        Path(tmp_path / "2.xml").touch()
        Path(tmp_path / "3.js").touch()

        bug = EnhancedBug(None, **bug_data)
        assert len(list(BrowserConfiguration.iterate(bug, tmp_path))) == 8


def test_js_configuration_iterate_001(mocker, bug_data):
    """Simple test JSConfiguration.iterate()"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        Path(tmp_path / "1.html").touch()
        Path(tmp_path / "2.xml").touch()
        Path(tmp_path / "3.js").touch()

        mock = mocker.patch(
            "bugmon.bug.EnhancedBug.runtime_opts", new_callable=mocker.PropertyMock
        )
        mock.return_value = []
        bug = EnhancedBug(None, **bug_data)
        assert len(list(JSConfiguration.iterate(bug, tmp_path))) == 6
