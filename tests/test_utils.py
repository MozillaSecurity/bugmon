# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at http://mozilla.org/MPL/2.0/.
import subprocess

import pytest

import bugmon.utils as utils


@pytest.mark.parametrize("returncode, expected", [(0, True), (1, False)])
def test_is_pernosco_available(mocker, returncode, expected):
    """Test is_pernosco_available with mocked subprocess.run."""
    mock_run = mocker.patch("bugmon.utils.subprocess.run")
    mock_run.return_value.returncode = returncode

    # Call the function and assert that it returns the expected result
    assert utils.is_pernosco_available() == expected
    mock_run.assert_called_once_with(
        ["pernosco-submit", "--help"],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def test_get_pernosco_trace_match(tmp_path):
    """Verify that get_pernosco_trace returns the correct path"""
    trace_path = tmp_path / "reports" / "1" / "rr-traces" / "latest-trace"
    trace_path.mkdir(parents=True)
    assert utils.get_pernosco_trace(tmp_path) == trace_path


def test_get_pernosco_trace_none_match(tmp_path):
    """Verify that get_pernosco_trace"""
    assert utils.get_pernosco_trace(tmp_path) is None


@pytest.mark.parametrize(
    "file_name, expected",
    [
        ("test.js", "test.js"),
        ("subdir/test.js", "subdir/test.js"),
        ("foo:bar.js", "foobar.js"),
        (r"subdir\\test.js", "subdir/test.js"),
    ],
)
def test_sanitize_attachment_path(tmp_path, file_name, expected):
    """Verify attachment paths are sanitized and remain relative."""
    assert utils.sanitize_attachment_path(tmp_path, file_name) == tmp_path / expected


@pytest.mark.parametrize(
    "file_name",
    [
        "",
        ".",
        "..",
        "../..",
        "../outside.js",
        ".. /outside.js",
        "..\x00/outside.js",
        "nested/./test.js",
        "nested/../test.js",
        "/absolute/path.js",
        "C:\\absolute\\path.js",
    ],
)
def test_sanitize_attachment_path_rejects_unsafe_paths(tmp_path, file_name):
    """Verify unsafe paths raise instead of being normalized."""
    with pytest.raises(ValueError, match="Unsafe attachment path"):
        utils.sanitize_attachment_path(tmp_path, file_name)


def test_sanitize_attachment_path_limits_error_length(tmp_path):
    """Verify unsafe filenames cannot produce excessively long errors."""
    with pytest.raises(ValueError) as exc_info:
        utils.sanitize_attachment_path(tmp_path, f"../{'x' * 1000}.js")

    assert len(str(exc_info.value)) <= 125
    assert str(exc_info.value).endswith("...")


def test_has_pernosco_creds_all(pernosco_creds):
    """Verify that has_pernosco_creds returns True when all creds present"""
    assert utils.has_pernosco_creds(pernosco_creds) is True


def test_has_pernosco_creds_partial(caplog):
    dictionary = {"PERNOSCO_USER": "value", "PERNOSCO_GROUP": "value"}
    assert utils.has_pernosco_creds(dictionary) is False
    expected = "Cannot find Pernosco env variable PERNOSCO_USER_SECRET_KEY!"
    assert caplog.messages[-1] == expected
