"""Standalone CLI controls for temporarily deferring Pernosco."""

import pytest

from bugmon.main import main, parse_args


@pytest.mark.parametrize("value, disabled", [(None, False), ("0", False), ("1", True)])
def test_disable_pernosco_environment(monkeypatch, value, disabled):
    monkeypatch.delenv("DISABLE_PERNOSCO", raising=False)
    if value is not None:
        monkeypatch.setenv("DISABLE_PERNOSCO", value)
    assert parse_args(["--bugs", "123"]).disable_pernosco is disabled
    assert parse_args(["--disable-pernosco", "--bugs", "123"]).disable_pernosco


def test_main_passes_disable_pernosco(monkeypatch, mocker, bug_data):
    monkeypatch.setenv("BZ_API_ROOT", "https://example.invalid/rest")
    monkeypatch.setenv("BZ_API_KEY", "key")
    client = mocker.patch("bugmon.main.Bugsy").return_value
    client.request.return_value = {"bugs": [bug_data]}
    monitor = mocker.patch("bugmon.main.BugMonitor")
    assert main(["--disable-pernosco", "--bugs", str(bug_data["id"])]) == 0
    assert monitor.call_args.kwargs["disable_pernosco"] is True
    monitor.return_value.process.assert_called_once_with(False)
