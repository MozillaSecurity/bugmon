# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at http://mozilla.org/MPL/2.0/.
import pytest

import bugmon.utils as utils


@pytest.mark.parametrize("binary", [True, False])
@pytest.mark.parametrize("library", [True, False])
def test_is_pernosco_available(binary, library, mocker, tmp_path):
    """Verify that is_pernosco_available returns true if both conditions are true"""
    bin_path = "/usr/bin/pernosco-submit" if binary else None
    mocker.patch("bugmon.utils.PERNOSCO", bin_path)

    if library:
        pernosco_shared = tmp_path / "pernoscoshared"
        pernosco_shared.mkdir()

    mocker.patch(
        "bugmon.utils.sysconfig.get_path",
        return_value=tmp_path,
    )

    expected = binary and library
    assert utils.is_pernosco_available() is expected


def test_get_pernosco_trace_match(tmp_path):
    """Verify that get_pernosco_trace returns the correct path"""
    trace_path = tmp_path / "reports" / "1" / "rr-traces" / "latest-trace"
    trace_path.mkdir(parents=True)
    assert utils.get_pernosco_trace(tmp_path) == trace_path


def test_get_pernosco_trace_none_match(tmp_path):
    """Verify that get_pernosco_trace"""
    assert utils.get_pernosco_trace(tmp_path) is None


def test_has_pernosco_creds_all(pernosco_creds):
    """Verify that has_pernosco_creds returns True when all creds present"""
    assert utils.has_pernosco_creds(pernosco_creds) is True


def test_has_pernosco_creds_partial(caplog):
    dictionary = {"PERNOSCO_USER": "value", "PERNOSCO_GROUP": "value"}
    assert utils.has_pernosco_creds(dictionary) is False
    expected = "Cannot find Pernosco env variable PERNOSCO_USER_SECRET_KEY!"
    assert caplog.messages[-1] == expected
