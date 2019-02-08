import pytest

from decimal import Decimal

import numpy as np

import qcelemental as qcel

_arrs = {
    'a1234_14': np.arange(4),
    'blip14': np.arange(4) + [0., 0.02, 0.005, 0.02],
    'a1234_22': np.arange(4).reshape((2, 2)),
    'blip22': (np.arange(4) + [0., 0.02, 0.005, 0.02]).reshape((2, 2)),
    'iblip14': np.arange(4) + [0, 1, 0, 1],
    'iblip22': (np.arange(4) + [0, 1, 0, 1]).reshape((2, 2)),
}

_pass_message = '\t{:.<66}PASSED'


@pytest.mark.parametrize("ref,cpd,tol,kw,boool,msg", [
    (2., 2.02, 1.e-1, {'label': 'asdf'}, True, (None,
        _pass_message.format('asdf'))),
    (2., 2.02, 1.e-2, {'label': 'asdf'}, False, (None,
        'asdf: computed value (2.0200) does not match (2.0000) to atol=0.01 by difference (0.0200).')),
    (2., Decimal("2.02"), 1.e-1, {'label': 'asdf'}, True, (None,
        _pass_message.format('asdf'))),
    (2., Decimal("2.02"), 1.e-2, {'label': 'asdf'}, False, (None,
        'asdf: computed value (2.0200) does not match (2.0000) to atol=0.01 by difference (0.0200).')),
    (2., 2.000000002, 1.e-9, {}, False, (None,
        'test_compare_values: computed value (2.00000000200) does not match (2.00000000000) to atol=1e-09 by difference (0.00000000200).')),
    (2., 2.05, 1.e-3, {}, False, (None,
        'test_compare_values: computed value (2.05000) does not match (2.00000) to atol=0.001 by difference (0.05000).')),
    (_arrs['a1234_14'], _arrs['blip14'], 1.e-1, {}, True, (None,
        _pass_message.format('test_compare_values'))),
    (_arrs['a1234_14'], _arrs['blip14'], 1.e-2, {}, False, (None,
        """test_compare_values: computed value does not match to atol=0.01.
  Expected:
    [0. 1. 2. 3.]
  Observed:
    [0.    1.02  2.005 3.02 ]
  Difference (passed elements are zeroed):
    [0.   0.02 0.   0.02]""")),
    (_arrs['a1234_22'], _arrs['blip22'], 1.e-1, {}, True, (None,
        _pass_message.format('test_compare_values'))),
    (_arrs['a1234_22'], _arrs['blip22'], 1.e-2, {}, False, (None,
        """test_compare_values: computed value does not match to atol=0.01.
  Expected:
    [[0. 1.]
     [2. 3.]]
  Observed:
    [[0.    1.02 ]
     [2.005 3.02 ]]
  Difference (passed elements are zeroed):
    [[0.   0.02]
     [0.   0.02]]""")),
    (_arrs['a1234_22'], _arrs['blip14'], 1.e-2, {}, False, (None,
        """test_compare_values: computed shape ((4,)) does not match ((2, 2)).""")),
    (None, None, 1.e-4, {'passnone': True}, True, (None,
        _pass_message.format('test_compare_values'))),
    (None, None, 1.e-4, {}, False, (None,
        """test_compare_values: computed value (nan) does not match (nan) to atol=0.0001 by difference (nan).""")),
])  # yapf: disable
def test_compare_values(ref, cpd, tol, kw, boool, msg):
    res, mstr = qcel.testing.compare_values(ref, cpd, **kw, atol=tol, return_message=True)
    print(res, mstr)
    assert res is boool
    assert mstr.strip() == msg[1].strip()


@pytest.mark.parametrize("ref,cpd,kw,boool,msg", [
    (2, 2, {'label': 'asdf'}, True, (None,
        _pass_message.format('asdf'))),
    (2, -2, {'label': 'asdf'}, False, (None,
        'asdf: computed value (-2) does not match (2) by difference (-4).')),
    (2, Decimal("2"), {'label': 'asdf'}, True, (None,
        _pass_message.format('asdf'))),
    (2, Decimal("3"), {'label': 'asdf'}, False, (None,
        'asdf: computed value (3) does not match (2) by difference (1).')),
    (True, True, {}, True, (None,
        _pass_message.format('test_compare'))),
    (False, False, {}, True, (None,
        _pass_message.format('test_compare'))),
    (None, None, {}, True, (None,
        _pass_message.format('test_compare'))),
    (True, None, {}, False, (None,
        'test_compare: computed value (None) does not match (True) by difference ((n/a)).')),
    (True, False, {}, False, (None,
        'test_compare: computed value (False) does not match (True) by difference ((n/a)).')),
    (False, None, {}, False, (None,
        'test_compare: computed value (None) does not match (False) by difference ((n/a)).')),
    (False, True, {}, False, (None,
        'test_compare: computed value (True) does not match (False) by difference ((n/a)).')),
    (None, False, {}, False, (None,
        'test_compare: computed value (False) does not match (None) by difference ((n/a)).')),
    (None, True, {}, False, (None,
        'test_compare: computed value (True) does not match (None) by difference ((n/a)).')),
    ('cat', 'cat', {}, True, (None,
        _pass_message.format('test_compare'))),
    ('cat', 'mouse', {}, False, (None,
        'test_compare: computed value (mouse) does not match (cat) by difference ((n/a)).')),
    (_arrs['a1234_14'], _arrs['a1234_14'], {}, True, (None,
        _pass_message.format('test_compare'))),
    (_arrs['a1234_14'], _arrs['iblip14'], {}, False, (None,
        """ test_compare: computed value does not match.
  Expected:
    [0 1 2 3]
  Observed:
    [0 2 2 4]
  Difference:
    [0 1 0 1]""")),
    (_arrs['a1234_22'], _arrs['a1234_22'], {}, True, (None,
        _pass_message.format('test_compare'))),
    (_arrs['a1234_22'], _arrs['iblip22'], {}, False, (None,
        """test_compare: computed value does not match.
  Expected:
    [[0 1]
     [2 3]]
  Observed:
    [[0 2]
     [2 4]]
  Difference:
    [[0 1]
     [0 1]]""")),
    (_arrs['a1234_22'], _arrs['iblip14'], {}, False, (None,
        """test_compare: computed shape ((4,)) does not match ((2, 2)).""")),
    (1, np.ones(1), {}, False, (None,
        """test_compare: computed shape ((1,)) does not match (()).""")),
    (1, np.array(1), {}, True, (None,
        _pass_message.format('test_compare'))),
    (1, np.array([1]), {}, False, (None,
        """test_compare: computed shape ((1,)) does not match (()).""")),
])  # yapf: disable
def test_compare(ref, cpd, kw, boool, msg):
    res, mstr = qcel.testing.compare(ref, cpd, **kw, return_message=True)
    assert res is boool
    assert mstr.strip() == msg[1].strip()
