# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at http://mozilla.org/MPL/2.0/.
from autobisect.bisect import BisectionResult
from bugsy import Bugsy

from bugmon import BugMonitor, ReproductionPassed, ReproductionCrashed
from bugmon.bug import EnhancedBug


def test_bugmon_need_info_on_bisect_fix(mocker, bugmon, build):
    """Test that the assignee is NI'd when the testcase no longer reproduces"""
    mocker.patch.object(bugmon, "detect_config", return_value=True)
    mocker.patch.object(
        bugmon,
        "_reproduce_bug",
        side_effect=[ReproductionPassed(build), ReproductionCrashed(build)],
    )
    bisect_result = mocker.Mock(BisectionResult, autospec=True)
    bisect_result.status = BisectionResult.SUCCESS
    mocker.patch.object(bugmon, "_bisect", return_value=bisect_result)
    mock_bug = mocker.MagicMock(EnhancedBug, autospec=True)
    bugmon.bug = mock_bug

    bugmon._confirm_open()

    assert mock_bug.add_needinfo.call_count == 1


def test_bugmon_pernosco_no_log_location(caplog, mocker, tmp_path, bug):
    """Verify that bugmon exits early if no log location is provided"""
    bugsy = mocker.Mock(Bugsy, autospec=True)
    bugmon = BugMonitor(bugsy, bug, tmp_path, dry_run=True)
    mock = mocker.patch.object(bugmon, "detect_config")
    bugmon.add_command("pernosco")
    bugmon.process()

    assert bugmon.log_location is None
    assert mock.called is False
    match = "Cannot record a pernosco session without a log location!"
    assert len([message for message in caplog.messages if match in message]) == 1


def test_bugmon_pernosco_no_config_identified(mocker, tmp_path, bugmon, js_config):
    """Verify that bugmon exits early when no configuration was identified"""
    bugmon.add_command("pernosco")
    bugmon.logs = tmp_path
    mocker.patch.object(bugmon, "detect_config", return_value=None)
    repro_spy = mocker.patch.object(bugmon, "_reproduce_bug")
    bugmon._pernosco()

    # Verify that we never tried to reproduce the bug
    assert repro_spy.called is False


def test_bugmon_pernosco_disallow_js_config(mocker, tmp_path, bugmon, js_config):
    """Verify that bugmon exits early when dealing with a JS bug configuration"""
    bugmon.add_command("pernosco")

    pernosco_submit = tmp_path / "pernosco_submit.py"
    pernosco_submit.touch()
    bugmon.pernosco_submit = pernosco_submit
    mocker.patch.object(bugmon, "detect_config", return_value=js_config)

    repro_spy = mocker.patch.object(bugmon, "_reproduce_bug")
    bugmon._pernosco()

    # Verify that we never tried to reproduce the bug
    assert repro_spy.called is False
    # Verify that the pernosco command is removed
    assert "pernosco" not in bugmon.bug.commands


def test_bugmon_pernosco_browser_bug_success(
    mocker, tmp_path, bugmon, build, browser_config
):
    """Verify that bugmon correctly reports a successful pernosco session"""
    bugmon.add_command("pernosco")
    mocker.patch.object(bugmon, "detect_config", return_value=browser_config)

    result = ReproductionCrashed(build)
    mocker.patch.object(bugmon, "_reproduce_bug", return_value=result)
    mocker.patch("bugmon.bugmon.find_pernosco_trace_dir", return_value=tmp_path)
    mocker.patch("bugmon.bugmon.shutil.make_archive", return_value=tmp_path)
    bugmon._pernosco()

    # Verify evaluator settings updated
    assert browser_config.evaluator.pernosco is True
    # Verify that the pernosco command is removed
    assert "pernosco" not in bugmon.bug.commands
    assert (bugmon.log_location / "build.json").exists
    assert (bugmon.log_location / "rr-trace.tar.gz").exists


def test_bugmon_pernosco_browser_bug_failure(
    mocker, tmp_path, bugmon, browser_config, build
):
    """Verify bugmon correctly reports when recording a pernosco session fails"""
    bugmon.add_command("pernosco")

    bugmon.logs = tmp_path
    mocker.patch.object(bugmon, "detect_config", return_value=browser_config)

    result = ReproductionPassed(build)
    mocker.patch.object(bugmon, "_reproduce_bug", return_value=result)
    bugmon._pernosco()

    # Verify that bugmon reports the failure
    assert len(bugmon.queue) == 1
    assert bugmon.queue[0] == "Failed to record an rr session for this bug."
    # Verify that the pernosco command is removed
    assert "pernosco" not in bugmon.bug.commands
