# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at http://mozilla.org/MPL/2.0/.

# pylint: disable=protected-access
import copy
import json
from types import SimpleNamespace

import pytest

from bugmon.bug import (
    BugException,
    EnhancedBug,
    LocalAttachment,
    LocalComment,
    sanitize_bug,
)

BRANCH_ALIAS_PAIRS = [
    ("central", 81),
    ("beta", 80),
    ("release", 79),
    ("esr78", 78),
    ("esr68", 68),
]

REV = "7bd6cb8b76c078f5e687574decdde97f1e4affce"
SHORT_REV = REV[:12]
BUILD_ID = f"20200811-{SHORT_REV}"
DATE = BUILD_ID[:8]


def test_new_attachment(attachment_data):
    """Test that new Attachment is the same as fixture"""
    result = LocalAttachment(**attachment_data).to_dict()

    for key in result:
        if key in ["last_change_time", "creation_time"]:
            result_date = result[key].strftime("%Y-%m-%dT%H:%M:%SZ")
            assert attachment_data[key] == result_date
        else:
            assert attachment_data[key] == result[key]


def test_new_comment(comment_data):
    """Test that new Comment is the same as fixture"""
    result = LocalComment(**comment_data).to_dict()
    for key in result:
        if key in ["time", "creation_time"]:
            result_date = result[key].strftime("%Y-%m-%dT%H:%M:%SZ")
            assert comment_data[key] == result_date
        elif key == "tags":
            assert comment_data[key] == list(result[key])
        else:
            assert comment_data[key] == result[key]


def test_new_bug(bug_data):
    """Test that new Bug is the same as fixture"""
    result = EnhancedBug(None, **bug_data).to_dict()
    for key in result:
        assert bug_data[key] == result[key]


def test_new_bug_without_bugsy_or_prefetch(bug_data_base):
    """Test that new Bug without bugsy or cached data throws"""
    with pytest.raises(BugException):
        EnhancedBug(None, **bug_data_base)


def test_new_bug_prefetch_exclusion(bug_data):
    """Test that new Bug with prefetch excludes attachments and comments"""
    result = EnhancedBug(None, **bug_data).to_dict()
    assert "attachments" not in result
    assert "comments" not in result


@pytest.mark.parametrize("method", ["add_attachment", "add_comment"])
def test_bug_remote_methods(bug_data, method):
    """Test that EnhancedBug with prefetch enabled throws on remote methods"""
    bug = EnhancedBug(bugsy=None, **bug_data)
    with pytest.raises(TypeError) as e:
        getattr(bug, method)(None)

    assert str(e.value) == "Method not supported when using a cached bug"


def test_bug_get_attachments_prefetch(attachment_data, bug_data):
    """Test that get_attachments with cached data returns correct attacment"""
    bug = EnhancedBug(bugsy=None, **bug_data)
    attachments = bug.get_attachments()
    assert len(attachments) == 1
    raw_data = json.loads(json.dumps(attachments[0], default=sanitize_bug))
    assert raw_data == attachment_data


def test_bug_get_comments_prefetch(bug_data, comment_data):
    """Test that get_attachments with cached data returns correct attacment"""
    bug = EnhancedBug(bugsy=None, **bug_data)
    comments = bug.get_comments()
    assert len(comments) == 1
    raw_data = json.loads(json.dumps(comments[0], default=sanitize_bug))
    assert raw_data == comment_data


@pytest.mark.parametrize("method", ["add_tags", "remove_tags"])
def test_comment_remote_methods(comment_data, method):
    """Test that LocalComment throws on remote methods"""
    comment = LocalComment(**comment_data)
    with pytest.raises(TypeError) as e:
        getattr(comment, method)(None)

    assert str(e.value) == "Method not supported when using a cached comment"


@pytest.mark.parametrize("method", ["update"])
def test_attachment_remote_methods(attachment_data, method):
    """Test that LocalAttachment throws on remote methods"""
    attachment = LocalAttachment(**attachment_data)
    with pytest.raises(TypeError) as e:
        getattr(attachment, method)()

    assert str(e.value) == "Method not supported when using a cached attachment"


@pytest.mark.parametrize("alias, version", BRANCH_ALIAS_PAIRS)
def test_bug_branch(mocker, bug_data, alias, version):
    """Test that branch matches alias of current version"""
    mocker.patch("bugmon.bug.Fetcher.resolve_esr", side_effect=["esr78", "esr68"])
    bug = EnhancedBug(bugsy=None, **bug_data)

    # Set fixed central version and bug version
    bug._central_version = 81
    bug._bug["version"] = version

    assert bug.branch == alias


def test_bug_branches(mocker, bug_data):
    """Test branch enumeration"""
    mocker.patch("bugmon.bug.Fetcher.resolve_esr", side_effect=["esr78", "esr68"])
    bug = EnhancedBug(bugsy=None, **bug_data)
    # Set fixed central version
    bug._central_version = 81

    for alias, version in bug.branches.items():
        if alias == "central":
            assert version == 81
        elif alias == "beta":
            assert version == 80
        elif alias == "release":
            assert version == 79
        elif alias == "esr78":
            assert version == 78
        elif alias == "esr68":
            assert version == 68


def test_bug_build_flags(bug_data):
    """Simple test of bug.build_flags"""
    data = copy.deepcopy(bug_data)
    data["comments"][0]["text"] = "Built with --enable-address-sanitizer --enable-debug"
    bug = EnhancedBug(bugsy=None, **data)

    assert bug.build_flags.asan
    assert bug.build_flags.debug
    assert bug.build_flags.tsan is False
    assert bug.build_flags.valgrind is False


def test_bug_central_version(mocker, bug_data):
    """Simple test of bug.central_version"""
    mocker.patch("bugmon.bug._get_milestone", return_value=81)
    bug = EnhancedBug(bugsy=None, **bug_data)

    assert bug.central_version == 81


def test_bug_comment_zero(bug_data):
    """Simple test of bug.comment_zero"""
    bug = EnhancedBug(bugsy=None, **bug_data)

    assert bug.comment_zero == bug_data["comments"][0]["text"]


@pytest.mark.parametrize("code_wrap", [True, False])
@pytest.mark.parametrize("bid", [REV, SHORT_REV, BUILD_ID, DATE, "INVALID_REV"])
def test_bug_initial_build_id_comment(mocker, bug_data, code_wrap, bid):
    """Test parsing of initial_build_id from comment"""
    if code_wrap:
        bid_str = f"`{bid}`"
    else:
        bid_str = bid

    data = copy.deepcopy(bug_data)
    data["comments"][0]["text"] = f"Found while fuzzing mozilla-central rev {bid_str}"
    bug = EnhancedBug(bugsy=None, **data)

    # Disable verification
    mocker.patch("bugmon.bug._get_rev", return_value=0)

    # Set fixed branch
    bug._branch = "mozilla-central"

    if bid == BUILD_ID:
        assert bug.initial_build_id == bid.split("-")[1]
    elif bid in (REV, SHORT_REV):
        assert bug.initial_build_id == SHORT_REV
    elif bid == DATE:
        mocker.patch("bugmon.bug.Fetcher").return_value = SimpleNamespace(
            **{"changeset": REV}
        )
        assert bug.initial_build_id == REV
    else:
        mocker.patch("bugmon.bug.Fetcher").side_effect = BugException
        with pytest.raises(BugException):
            _ = bug.initial_build_id


@pytest.mark.parametrize("bid", [REV, SHORT_REV])
def test_bug_initial_build_id_whiteboard(mocker, bug_data, bid):
    """Test parsing of initial_build_id from whiteboard"""
    data = copy.deepcopy(bug_data)
    data["whiteboard"] = f"[bugmon:origRev={bid}]"
    bug = EnhancedBug(bugsy=None, **data)

    # Disable verification
    mocker.patch("bugmon.bug._get_rev", return_value=0)

    # Set fixed branch
    bug._branch = "central"

    assert bug.initial_build_id == SHORT_REV


@pytest.mark.parametrize("use_trunk", [True, False])
def test_bug_version(mocker, bug_data, use_trunk):
    """Simple test of version helper"""
    if use_trunk:
        bug = EnhancedBug(bugsy=None, **bug_data)
        mocker.patch("bugmon.bug._get_milestone", return_value=81)
    else:
        data = copy.deepcopy(bug_data)
        data["version"] = 81
        bug = EnhancedBug(bugsy=None, **data)

    assert bug.version == 81


def test_bug_command_setter_append(bug_data):
    """Test appending commands to whiteboard"""
    bug = EnhancedBug(bugsy=None, **bug_data)
    commands = bug.commands
    commands["fake_command"] = None
    bug.commands = commands
    assert bug.whiteboard == "[bugmon:bisected,confirmed,verified,fake_command]"


def test_bug_command_setter_replace(bug_data):
    """Test replacing commands"""
    bug = EnhancedBug(bugsy=None, **bug_data)
    bug.commands = {"fake_command": None}

    assert bug.whiteboard == "[bugmon:fake_command]"


def test_bug_command_setter_empty_bugmon(bug_data):
    """Test setting command where bugmon exists on whiteboard with no commands"""
    data = copy.deepcopy(bug_data)
    data["whiteboard"] = "[bugmon:]"
    bug = EnhancedBug(bugsy=None, **data)
    bug.commands = {"fake_command": None}

    assert bug.whiteboard == "[bugmon:fake_command]"


def test_bug_command_setter_empty_whiteboard(bug_data):
    """Test initialization of bugmon command on whiteboard"""
    data = copy.deepcopy(bug_data)
    data["whiteboard"] = ""
    bug = EnhancedBug(bugsy=None, **data)
    bug.commands = {"fake_command": None}

    assert bug.whiteboard == "[bugmon:fake_command]"


def test_bug_command_setter_remove_command(bug_data):
    """Test removing command from whiteboard"""
    data = copy.deepcopy(bug_data)
    data["whiteboard"] = "[something-else][bugmon:verify]"
    bug = EnhancedBug(bugsy=None, **data)
    bug.commands = {}

    assert bug.whiteboard == "[something-else]"


def test_bug_cache_bug(mocker, bug_data_base, comment_data, attachment_data):
    """Test EnhancedBug.cache_bug()"""
    data = copy.deepcopy(bug_data_base)
    bug = EnhancedBug(bugsy=True, **data)

    attachments = [LocalAttachment(**attachment_data)]
    mocker.patch("bugmon.bug.EnhancedBug.get_attachments", return_value=attachments)
    comments = [LocalComment(**comment_data)]
    mocker.patch("bugmon.bug.EnhancedBug.get_comments", return_value=comments)

    cached_bug = EnhancedBug.cache_bug(bug)
    assert cached_bug.get_attachments() == attachments
    assert cached_bug.get_comments() == comments


@pytest.mark.parametrize("has_assignee", [True, False])
def test_bug_assignee(bug_data, has_assignee):
    """Test that bug returns the correct assignee"""
    data = copy.deepcopy(bug_data)

    if not has_assignee:
        data["assigned_to"] = "nobody@mozilla.com"

    bug = EnhancedBug(bugsy=None, **data)

    expected = "creator" if not has_assignee else "assigned_to"
    assert bug.assignee == data[f"{expected}_detail"]


def test_bug_add_needinfo(bug_data):
    """Test that needinfo can be added to a bug"""
    data = copy.deepcopy(bug_data)
    bug = EnhancedBug(bugsy=None, **data)
    bug.add_needinfo("abc@mozilla.com")

    expected = {
        "is_multiplicable": True,
        "name": "needinfo",
        "requestee": "abc@mozilla.com",
        "status": "?",
    }
    assert bug.flags[0] == expected
