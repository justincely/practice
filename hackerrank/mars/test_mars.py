import hackerrank_practice as hp
import numpy as np

from nose.tools import assert_raises

#-------------------------------------------------------------------------------

def test_given_cases():
    assert hp.optimal_time(open('input000.txt').read()) == \
        float(open('output000.txt').read()), "test-case 0 failed"
    
    assert hp.optimal_time(open('input001.txt').read()) == \
        float(open('output001.txt').read()), "test-case 1 failed"

#-------------------------------------------------------------------------------

def test_read_time():
    assert hp.read_time(10, 10, 10) == 21, "wrong time calculated!"
    assert hp.read_time(10.0, 10.0, 10.0) == 21, "wrong time calculated!"

#-------------------------------------------------------------------------------

def test_byte_check_types():
    chunks = [(0, 10), (10, 30), (30, 50), (50, 100)]
    assert hp.byte_check(100, chunks), "Didn't work with int"
    assert hp.byte_check(range(100), chunks), "Didn't work with list"
    assert hp.byte_check(set(range(100)), chunks), "Didn't work with set"
    assert hp.byte_check(tuple(range(100)), chunks), "Didn't work with tuple"

#-------------------------------------------------------------------------------

def test_byte_check_pass():
    overlapping = [(0, 20), (10, 20), (5, 40)]
    assert hp.byte_check(40, overlapping), "Didn't work with overlapping values"

    single = [(0, 20)]
    assert hp.byte_check(20, single), "Didn't work with single chunk"

#-------------------------------------------------------------------------------

def test_byte_check_fail():
    gap = [(0, 20), (21, 40), (40, 80)]
    assert not hp.byte_check(80, gap), "Didn't work with gapped data"

    wrong_range = [(0, 20), (40, 80), (80, 100)]
    assert not hp.byte_check(80, wrong_range), "Didn't work with wrong range"

#-------------------------------------------------------------------------------

def test_bad_lines():
    assert hp.optimal_time(open('crap_input.txt').read()) == \
        float(open('output000.txt').read()), "crap test-case 0 failed"

#-------------------------------------------------------------------------------

def test_ucs():
    cost_data = {(0,200):5,
                 (200,400):5,
                 (400,600):5,
                 (600,800):5,
                 (800,1000):5,
                 (0, 2000):3,
                 (1000,2000):5}

    nbytes = 2000

    assert hp.uniform_cost_search(cost_data, nbytes) == 3, 'nope'

    cost_data[(0, 500)] = 1
    cost_data[(500, 2000)] = 1

    assert hp.uniform_cost_search(cost_data, nbytes) == 2, 'nope'

    cost_data = {(0, 2000):3}

    assert hp.uniform_cost_search(cost_data, nbytes) == 3, 'nope'

    cost_data = {(1,200):5}

    assert hp.uniform_cost_search(cost_data, nbytes) == None, 'nope'

#-------------------------------------------------------------------------------
