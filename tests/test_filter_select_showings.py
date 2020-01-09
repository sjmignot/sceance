from datetime import datetime, date, time
import pytest
import sceance.filter_select_showings

testdata = [
    ([0, datetime.combine(date(2020, 1, 8), time(12, 0))], False),
    ([0, datetime.combine(date(2020, 1, 8), time(20, 0))], True),
    ([0, datetime.combine(date(2020, 1, 5), time(16, 0))], True),
    ([0, datetime.combine(date(2020, 1, 5), time(10, 0))], True),
]

@pytest.mark.parametrize("a,expected", testdata)
def test_not_during_work_for_workday(a, expected):
    assert sceance.filter_select_showings.not_during_work(a) == expected
