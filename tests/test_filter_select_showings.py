from datetime import datetime, date, time
import pytest
import sceance.filter_select_showings
import argparse

# Monday-Friday
WORKDAYS = {0,1,2,3,4}

# 9-5
WORKHOURS = ((9,0),(17,0))

testdata = [
    ([0, datetime.combine(date(2020, 1, 8), time(12, 0))], WORKDAYS, WORKHOURS, False),
    ([0, datetime.combine(date(2020, 1, 8), time(20, 0))], WORKDAYS, WORKHOURS, True),
    ([0, datetime.combine(date(2020, 1, 5), time(16, 0))], WORKDAYS, WORKHOURS, True),
    ([0, datetime.combine(date(2020, 1, 5), time(10, 0))], WORKDAYS, WORKHOURS, True)
]

@pytest.mark.parametrize("a,b,c,expected", testdata)
def test_not_during_work_for_workday(a, b, c ,expected):
    assert sceance.filter_select_showings.not_during_work(a, b, c) == expected
