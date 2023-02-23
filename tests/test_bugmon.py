# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at http://mozilla.org/MPL/2.0/.
import pytest
from autobisect.bisect import BisectionResult

from bugmon import BugMonitor, ReproductionCrashed, ReproductionPassed
from bugmon.bug import EnhancedBug
from bugmon.exceptions import BugmonException


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


def test_bugmon_throws_without_pernosco_submit(bug, bugsy, pernosco_creds, working_dir):
    """Test that bugmon throws when pernosco-submit is not available"""
    expected = "pernosco-submit is not properly configured!"
    with pytest.raises(BugmonException, match=expected):
        BugMonitor(bugsy, bug, working_dir, pernosco_creds, False)


def test_bugmon_pernosco_no_config_identified(mocker, tmp_path, bugmon):
    """Verify that bugmon exits early when no configuration was identified"""
    bugmon.add_command("pernosco")
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


def test_bugmon_pernosco_browser_bug_crashed(mocker, bugmon, build, browser_config):
    """Verify that bugmon correctly reports a successful pernosco session"""
    bugmon.add_command("pernosco")
    mocker.patch.object(bugmon, "detect_config", return_value=browser_config)

    result = ReproductionCrashed(build)
    mocker.patch.object(bugmon, "_reproduce_bug", return_value=result)

    trace_path = bugmon.log_dir / "reports" / "1" / "rr-traces" / "latest-trace"
    trace_path.mkdir(parents=True)
    bugmon._pernosco()

    # Verify evaluator settings updated
    assert browser_config.evaluator.pernosco is True
    # Verify that build.json was generated
    assert len(list(bugmon.log_dir.rglob("build.json"))) == 1
    # Verify that the pernosco command is removed
    assert "pernosco" not in bugmon.bug.commands


def test_bugmon_pernosco_browser_bug_failure(
    mocker,
    tmp_path,
    bugmon,
    browser_config,
    build,
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
    assert (
        bugmon.queue[0]
        == "Bugmon was unable to record a pernosco session for this bug."
    )
    # Verify that the pernosco command is removed
    assert "pernosco" not in bugmon.bug.commands


def test_bugmon_pernosco_failed_to_find_trace(
    caplog, mocker, browser_config, bugmon, build
):
    mocker.patch.object(bugmon, "detect_config", return_value=browser_config)
    result = ReproductionCrashed(build)
    mocker.patch.object(bugmon, "_reproduce_bug", return_value=result)
    bugmon._pernosco()

    assert caplog.messages[-1] == "Unable to identify a pernosco trace!"


def test_bugmon_pernosco_no_creds(browser_config, bugmon, build, caplog, mocker):
    bugmon.dry_run = False
    mocker.patch.object(bugmon, "detect_config", return_value=browser_config)
    result = ReproductionCrashed(build)
    mocker.patch.object(bugmon, "_reproduce_bug", return_value=result)

    trace_path = bugmon.log_dir / "reports" / "1" / "rr-traces" / "latest-trace"
    trace_path.mkdir(parents=True)

    bugmon._pernosco()

    assert caplog.messages[-1] == "Pernosco creds required for submitting traces!"


def test_bugmon_add_command(bugmon):
    """Test that add_command updates the whiteboard"""
    bugmon.bug.whiteboard = "[some-command]"
    bugmon.add_command("bisected")
    bugmon.add_command("confirmed")

    assert bugmon.bug.whiteboard == "[some-command][bugmon:bisected,confirmed]"


@pytest.mark.parametrize("status", ["ASSIGNED", "NEW", "UNCONFIRMED", "REOPENED"])
def test_bugmon_needs_confirm_status(status, bugmon):
    """Test that bug is confirmed based on status"""
    bugmon.bug.status = status
    bugmon.remove_command("confirmed")
    assert bugmon.needs_confirm() is True


@pytest.mark.parametrize("status", ["ASSIGNED", "NEW", "UNCONFIRMED", "REOPENED"])
def test_bugmon_already_confirmed(status, bugmon):
    """Test that bug is not reconfirmed"""
    bugmon.bug.status = status
    bugmon.add_command("confirmed")
    assert bugmon.needs_confirm() is False


@pytest.mark.parametrize("status", ["ASSIGNED", "NEW", "UNCONFIRMED", "REOPENED"])
def test_bugmon_confirm_requested(status, bugmon):
    """Test that bug is confirmed when requested regardless if it was already confirmed"""
    bugmon.bug.status = status
    bugmon.add_command("analyze")
    bugmon.add_command("confirmed")
    assert bugmon.needs_confirm() is True


def test_bugmon_needs_verify_status(bugmon):
    """Test that bug is verified based on status"""
    bugmon.bug.status = "RESOLVED"
    bugmon.bug.resolution = "FIXED"
    bugmon.remove_command("verified")
    assert bugmon.needs_verify() is True


def test_bugmon_already_verified(bugmon):
    """Test that bug is not re-verified"""
    bugmon.bug.status = "RESOLVED"
    bugmon.bug.resolution = "FIXED"
    bugmon.add_command("verified")
    assert bugmon.needs_verify() is False


def test_bugmon_verify_requested(bugmon):
    """Test that bug is verified when requested regardless if it was already verified"""
    bugmon.bug.status = "RESOLVED"
    bugmon.bug.resolution = "FIXED"
    bugmon.add_command("analyze")
    bugmon.add_command("verified")
    assert bugmon.needs_verify() is True
