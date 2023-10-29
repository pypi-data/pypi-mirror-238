# pylint: disable=C0114,C0116

import pytest


@pytest.mark.parametrize("option", ["-t", "--title"])
def test_debug_logs(cli_runner, csv_file, option):
    csv = csv_file("sample.csv")
    ret = cli_runner(csv, "-d", option, "my title is foobar")
    assert "title='my title is foobar'" in ret.stderr
    assert "my title is foobar" in ret.stderr


def test_default_title(cli_runner, csv_file):
    csv = csv_file("sample.csv")
    ret = cli_runner(csv, "-d")
    assert "Total Daily Walking Steps Count Up to Week" in ret.stderr


def test_default_title_on_last_week_of_the_year(cli_runner, csv_file):
    csv = csv_file("sample.csv")
    ret = cli_runner(csv, "-d", "-wk", "52")
    assert "Total Daily Walking Steps Count for the Year" in ret.stderr
