# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at http://mozilla.org/MPL/2.0/.
import base64
import io
import zipfile

import pytest
from autobisect.bisect import BisectionResult
from fuzzfetch import Platform

from bugmon import BugMonitor, ReproductionCrashed, ReproductionPassed
from bugmon.bug import EnhancedBug
from bugmon.exceptions import BugmonException


def _attachment(file_name, data, creation_time="2020-06-30T12:40:45Z"):
    attachment = type("Attachment", (), {})()
    attachment.file_name = file_name
    attachment.data = base64.b64encode(data).decode()
    attachment.creation_time = creation_time
    attachment.content_type = "text/plain"
    attachment.is_obsolete = False
    return attachment


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


def test_bugmon_throws_without_pernosco_submit(
    bug,
    bugsy,
    pernosco_creds,
    working_dir,
    mocker,
):
    """Test that bugmon throws when pernosco-submit is not available"""
    mock_run = mocker.patch("bugmon.utils.subprocess.run")
    mock_run.return_value.returncode = -1

    expected = "pernosco-submit is not properly configured!"
    with pytest.raises(BugmonException, match=expected):
        BugMonitor(bugsy, bug, working_dir, pernosco_creds, False)


def test_bugmon_fetch_attachments_preserves_nested_paths(mocker, bugmon):
    """Verify valid ZIP and regular attachments preserve nested paths."""
    archive_data = io.BytesIO()
    with zipfile.ZipFile(archive_data, "w") as archive:
        archive.writestr("nested/test.js", b"nested")
        archive.writestr("nested/", b"")

    attachments = [
        _attachment("attachments.zip", archive_data.getvalue()),
        _attachment("other/regular.js", b"regular", "2020-07-01T12:40:45Z"),
    ]
    mocker.patch("bugmon.bug.EnhancedBug.get_attachments", return_value=attachments)

    bugmon.fetch_attachments()

    assert (bugmon.test_dir / "nested/test.js").read_bytes() == b"nested"
    assert (bugmon.test_dir / "other/regular.js").read_bytes() == b"regular"


def test_bugmon_fetch_attachments_rejects_unsafe_path(mocker, bugmon):
    """Verify unsafe attachment paths raise instead of being normalized."""
    archive_data = io.BytesIO()
    with zipfile.ZipFile(archive_data, "w") as archive:
        archive.writestr("../escaped.js", b"escaped")

    attachments = [_attachment("attachments.zip", archive_data.getvalue())]
    mocker.patch("bugmon.bug.EnhancedBug.get_attachments", return_value=attachments)

    with pytest.raises(ValueError, match="Unsafe attachment path"):
        bugmon.fetch_attachments()

    assert not (bugmon.test_dir / "escaped.js").exists()
    assert not (bugmon.test_dir.parent / "escaped.js").exists()


def test_bugmon_no_need_pernosco_with_pernosco_failed(bugmon):
    """Test that bugmon does not attempt to record a pernosco session when the
    pernosco-failed status command is present"""
    bugmon.add_command("pernosco-failed")
    assert bugmon.needs_pernosco() is False


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


@pytest.mark.vcr()
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


@pytest.mark.vcr()
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


@pytest.mark.vcr()
def test_bugmon_pernosco_failed_to_find_trace(
    caplog,
    mocker,
    browser_config,
    bugmon,
    build,
):
    mocker.patch.object(bugmon, "detect_config", return_value=browser_config)
    result = ReproductionCrashed(build)
    mocker.patch.object(bugmon, "_reproduce_bug", return_value=result)
    bugmon._pernosco()

    assert caplog.messages[-1] == "Unable to identify a pernosco trace!"


@pytest.mark.vcr()
def test_bugmon_pernosco_x86(bugmon):
    """Verify bugmon reports that pernosco is not supported for x86 bugs"""
    bugmon.add_command("pernosco")
    bugmon.bug.keywords.append("pernosco-wanted")

    bugmon.bug._platform = Platform("Linux", "x86")
    bugmon._pernosco()

    assert len(bugmon.queue) == 1
    assert bugmon.queue[0] == "Pernosco is only supported for Linux x86_64 bugs."
    assert "pernosco" not in bugmon.bug.commands
    assert "pernosco-wanted" not in bugmon.bug.keywords


@pytest.mark.vcr()
def test_bugmon_pernosco_no_creds(browser_config, bugmon, build, caplog, mocker):
    bugmon.dry_run = False
    mocker.patch.object(bugmon, "detect_config", return_value=browser_config)
    result = ReproductionCrashed(build)
    mocker.patch.object(bugmon, "_reproduce_bug", return_value=result)

    trace_path = bugmon.log_dir / "reports" / "1" / "rr-traces" / "latest-trace"
    trace_path.mkdir(parents=True)

    bugmon._pernosco()

    assert caplog.messages[-1] == "Pernosco creds required for submitting traces!"


@pytest.mark.vcr()
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


def test_bugmon_already_verified_but_not_branches(bugmon):
    """Test that bug is verified if the branches have not been confirmed"""
    bugmon.bug.status = "VERIFIED"
    bugmon.bug.resolution = "FIXED"
    # patch branches to match the bug fixture
    bugmon.bug._branches = {
        "central": 80,
        "beta": 79,
        "release": 78,
    }
    assert bugmon.needs_verify() is True


@pytest.mark.parametrize("request_kind", ["command", "keyword"])
@pytest.mark.parametrize("action", ["confirm", "verify", "bisect", None])
def test_disabled_pernosco_preserves_pending_work(
    bugmon, mocker, request_kind, action, caplog
):
    """Deferred recording preserves requests and suppresses close-out comments."""
    bugmon.disable_pernosco = True
    if request_kind == "command":
        bugmon.add_command("pernosco")
    else:
        bugmon.bug.keywords.append("pernosco-wanted")
    mocker.patch.object(bugmon, "is_supported", return_value=True)
    for candidate in ("verify", "confirm", "bisect"):
        mocker.patch.object(
            bugmon, f"needs_{candidate}", return_value=candidate == action
        )

    def finish_analysis():
        bugmon._close_bug = True
        bugmon.report("Analysis completed.")

    methods = {
        "confirm": "_confirm_open",
        "verify": "_verify_fixed",
        "bisect": "_bisect",
    }
    analysis = None
    if action is not None:
        analysis = mocker.patch.object(
            bugmon, methods[action], side_effect=finish_analysis
        )
    record = mocker.patch.object(bugmon, "_pernosco")
    submit = mocker.patch("bugmon.bugmon.submit_pernosco")
    bugmon.process()

    record.assert_not_called()
    submit.assert_not_called()
    assert "bugmon" in bugmon.bug.keywords
    assert "pernosco-failed" not in bugmon.bug.commands
    if request_kind == "command":
        assert "pernosco" in bugmon.bug.commands
    else:
        assert "pernosco-wanted" in bugmon.bug.keywords
    diff = bugmon.bug.diff()
    if action is not None:
        analysis.assert_called_once_with()
        assert diff["comment"]["body"] == "Analysis completed."
    else:
        assert "comment" not in diff
    assert "Removing bugmon" not in caplog.text
    assert not bugmon.needs_pernosco()
    bugmon.disable_pernosco = False
    assert bugmon.needs_pernosco()
    bugmon.process()
    record.assert_called_once_with()


@pytest.mark.parametrize("terminal", ["unsupported", "failed"])
def test_disabled_pernosco_retains_terminal_cleanup(bugmon, mocker, terminal):
    """Requests that cannot be fulfilled do not prevent normal cleanup."""
    bugmon.disable_pernosco = True
    bugmon.add_command("pernosco")
    if terminal == "failed":
        bugmon.add_command("pernosco-failed")
    bugmon._close_bug = True
    mocker.patch.object(bugmon, "is_supported", return_value=terminal != "unsupported")
    for action in ("verify", "confirm", "bisect"):
        mocker.patch.object(bugmon, f"needs_{action}", return_value=False)
    record = mocker.patch.object(bugmon, "_pernosco")
    bugmon.process()
    record.assert_not_called()
    assert "bugmon" not in bugmon.bug.keywords
    assert "Removing bugmon keyword" in bugmon.bug.diff()["comment"]["body"]


def test_disabled_pernosco_skips_submit_validation(
    bug, bugsy, working_dir, pernosco_creds, mocker
):
    """Disabled recording does not require an installed submit utility."""
    available = mocker.patch("bugmon.bugmon.is_pernosco_available", return_value=False)
    monitor = BugMonitor(bugsy, bug, working_dir, pernosco_creds, disable_pernosco=True)
    available.assert_not_called()
    assert monitor.needs_pernosco() is False


@pytest.mark.parametrize(
    "resolution", ["DUPLICATE", "INVALID", "WORKSFORME", "WONTFIX"]
)
def test_disabled_pernosco_cleans_up_terminal_resolution(bugmon, resolution):
    """Terminal resolutions retain normal cleanup despite a pending request."""
    bugmon.disable_pernosco = True
    bugmon.add_command("pernosco")
    bugmon.bug.resolution = resolution
    bugmon.process()
    assert "bugmon" not in bugmon.bug.keywords
    assert "Removing bugmon keyword" in bugmon.bug.diff()["comment"]["body"]
