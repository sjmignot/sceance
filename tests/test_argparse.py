from datetime import datetime, date, time
import pytest
import sceance.__main__
import argparse
from contextlib import nullcontext as does_not_raise

timezone_testdata = [
    ('Europe', pytest.raises(argparse.ArgumentError)),
    (True, pytest.raises(argparse.ArgumentError)),
    ('Europe/Paris', does_not_raise),
    (None, pytest.raises(argparse.ArgumentError))
]

@pytest.mark.parametrize("a,expected", timezone_testdata)
def test_valid_timezone(a, expected):
    with expected:
        assert sceance.__main__.valid_timezone(a) is not None
