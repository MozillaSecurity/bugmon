# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at http://mozilla.org/MPL/2.0/.
from autobisect.bisect import BisectionResult
from autobisect.evaluators import EvaluatorResult

from bugmon import ReproductionResult
from bugmon.bug import EnhancedBug


def test_bugmon_need_info_on_bisect_fix(mocker, bugmon):
    """Test that the assignee is NI'd when the testcase no longer reproduces"""
    mocker.patch.object(bugmon, "detect_config", return_value=True)
    mocker.patch.object(
        bugmon,
        "_reproduce_bug",
        side_effect=[
            ReproductionResult(EvaluatorResult.BUILD_PASSED),
            ReproductionResult(EvaluatorResult.BUILD_CRASHED),
        ],
    )
    bisect_result = mocker.Mock(BisectionResult, autospec=True)
    bisect_result.status = BisectionResult.SUCCESS
    mocker.patch.object(bugmon, "_bisect", return_value=bisect_result)
    mock_bug = mocker.MagicMock(EnhancedBug, autospec=True)
    bugmon.bug = mock_bug

    bugmon._confirm_open()

    assert mock_bug.add_needinfo.call_count == 1
