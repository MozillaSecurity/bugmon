# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at http://mozilla.org/MPL/2.0/.
import copy
from pathlib import Path

import pytest
from bugmon import BugMonitor
from bugmon.bug import EnhancedBug
from bugsy import Bugsy

REV = "7bd6cb8b76c078f5e687574decdde97f1e4affce"
SHORT_REV = REV[:12]
BUILD_ID = f"20200811-{SHORT_REV}"

ATTACHMENT = {
    "flags": [],
    "attacher": "foobar@example.com",
    "last_change_time": "2020-06-30T12:40:45Z",
    "creation_time": "2020-06-30T12:40:45Z",
    "is_patch": 0,
    "description": "Testcase",
    "creator_detail": {
        "real_name": "Foo Bar (foobar)",
        "email": "foobar@example.com",
        "id": 123456,
        "name": "foobar@example.com",
        "nick": "foobar",
    },
    "is_obsolete": 0,
    "data": "YWxlcnQoMSkK",
    "content_type": "text/plain",
    "summary": "Testcase",
    "creator": "foobar@example.com",
    "id": 123456,
    "size": 10,
    "is_private": 0,
    "bug_id": 123456,
    "file_name": "test.js",
}

COMMENT = {
    "id": 123456,
    "is_private": False,
    "time": "2020-06-30T12:40:45Z",
    "creation_time": "2020-06-30T12:40:45Z",
    "bug_id": 123456,
    "text": "Found while fuzzing mozilla-central rev 72f0cfd2cd42 (built with --enable-debug).",
    "tags": [],
    "creator": "foobar@example.com",
    "attachment_id": None,
    "count": 0,
}

BUG = {
    "cf_webcompat_priority": "---",
    "cf_tracking_firefox79": "-",
    "keywords": ["assertion", "testcase"],
    "cf_tracking_thunderbird_esr68": "---",
    "op_sys": "Linux",
    "cf_status_thunderbird_esr60": "---",
    "creator": "foobar@example.com",
    "groups": ["core-security-release"],
    "is_confirmed": True,
    "cf_tracking_firefox80": "+",
    "cf_status_firefox_esr78": "affected",
    "cf_has_regression_range": "---",
    "whiteboard": "[bugmon:confirmed,verify]",
    "cf_tracking_firefox_sumo": "---",
    "duplicates": [],
    "regressed_by": [123456],
    "assigned_to": "foobar@example.com",
    "update_token": "1234567890",
    "cf_qa_whiteboard": "",
    "is_cc_accessible": True,
    "is_creator_accessible": True,
    "cf_tracking_thunderbird_esr78": "---",
    "classification": "Components",
    "component": "JavaScript Engine",
    "is_open": True,
    "severity": "S2",
    "cf_status_thunderbird_esr78": "---",
    "cf_status_firefox80": "affected",
    "priority": "P1",
    "cf_root_cause": "---",
    "cf_status_firefox79": "wontfix",
    "cf_status_thunderbird_esr68": "---",
    "cf_tracking_thunderbird_esr60": "---",
    "version": "Trunk",
    "cf_tracking_firefox_esr68": "---",
    "url": "",
    "cf_tracking_firefox_esr78": "80+",
    "mentors_detail": [],
    "votes": 0,
    "product": "Core",
    "cf_fx_iteration": "---",
    "cf_has_str": "---",
    "cf_fission_milestone": "---",
    "see_also": [],
    "cc": [],
    "creator_detail": {
        "nick": "foobar",
        "real_name": "Foo Bar (:foobar)",
        "email": "foobar@example.com",
        "id": 123456,
        "name": "foobar@example.com",
    },
    "cf_status_firefox78": "wontfix",
    "last_change_time": "2020-07-22T19:39:31Z",
    "creation_time": "2020-07-07T06:56:12Z",
    "cf_fx_points": "---",
    "target_milestone": "mozilla80",
    "cf_status_firefox_esr68": "unaffected",
    "depends_on": [],
    "platform": "x86_64",
    "flags": [],
    "id": 123456,
    "cf_tracking_firefox78": "---",
    "cf_tracking_firefox_relnote": "---",
    "assigned_to_detail": {
        "name": "foobar@example.com",
        "email": "foobar@example.com",
        "id": 123456,
        "real_name": "Foo Bar [:foobar]",
        "nick": "foobar",
    },
    "cf_crash_signature": "",
    "dupe_of": None,
    "type": "defect",
    "status": "ASSIGNED",
    "comment_count": 20,
    "summary": "Crash",
    "cf_user_story": "",
    "resolution": "",
    "blocks": [],
    "cf_last_resolved": "2020-07-20T22:04:28Z",
    "alias": None,
    "regressions": [],
    "mentors": [],
    "qa_contact": "",
    "cf_rank": None,
    "cc_detail": [],
}


@pytest.fixture(scope="module")
def attachment_fixture():
    """Simple attachment"""
    return ATTACHMENT


@pytest.fixture(scope="module")
def comment_fixture():
    """Simple comment"""
    return COMMENT


@pytest.fixture(scope="module")
def bug_fixture():
    """Simple bug"""
    return BUG


@pytest.fixture(scope="module")
def bug_fixture_prefetch():
    """Simple bug including attachment and comment data"""
    bug_data = copy.deepcopy(BUG)
    bug_data["attachments"] = [ATTACHMENT]
    bug_data["comments"] = [COMMENT]
    return bug_data


@pytest.fixture
def mock_bugmon(mocker, tmpdir, request, bug_fixture_prefetch):
    """Yields a mock bugmon instance"""
    bugsy = mocker.Mock(Bugsy, autospec=True)
    bug = EnhancedBug(None, **bug_fixture_prefetch)
    dry_run = request.param if hasattr(request, "param") else True
    yield BugMonitor(bugsy, bug, Path(tmpdir), dry_run)
