# -*- coding: utf-8 -*-
import pytest
from map_numbers_lb.map_numbers import *

@pytest.fixture
def cardinals():
    return load_number_map('constants/cardinal.txt')

@pytest.fixture
def ordinals():
    return load_number_map('constants/ordinal.txt')

@pytest.fixture
def months():
    return load_months('constants/months.txt')

def test_strip_punctuation():
    a = "100.000,76"
    a_desired = "10000076"
    assert strip_punctuation(a) == a_desired


def test_int2txt(cardinals):
    a = '651'
    a_txt = 'sechs honnert een a fofzeg'
    b = '311000'
    b_punct = '311.000'
    b_txt = "dräi honnert eelef dausend"
    c = '77248931'
    c_txt = 'siwen a siwwenzeg millioun zwee honnert aacht a véierzeg dausend néng honnert een a drësseg'
    u, t, s = cardinals

    assert int2txt(a, u, t, s) == a_txt
    assert int2txt(b, u, t, s) == b_txt
    assert int2txt(strip_punctuation(b_punct), u, t, s) == b_txt
    assert int2txt(c, u, t, s) == c_txt


def test_is_date(months):
    a = '2. Juli 2014'
    a_desired = True
    b = '2013'
    b_desired = True
    c = '99'
    c_desired = False
    d = '02.03.1784'
    d_desired = True
    e = "101 1955"
    e_desired = False
    f = "1989. 2011"
    f_desired = False
    g = "190 Fäll 2011"
    g_desired = False

    assert is_date(a, months) == a_desired
    assert is_date(b, months) == b_desired
    assert is_date(c, months) == c_desired
    assert is_date(d, months) == d_desired
    assert is_date(e, months) == e_desired
    assert is_date(f, months) == f_desired


def test_date2txt(cardinals, months):
    units, tens, scales = cardinals
    a = '2. Juli 1999'
    a_desired = "zweeten Juli nonzéng honnert néng a nonzeg"
    b = '21.03.2015'
    b_desired = 'een a zwanzegsten Mäerz zweedausend fofzéng'
    c = '15 09 1635'
    c_desired = 'fofzéngten September siechzéng honnert fënnef a drësseg'
    d = '1985 '
    d_desired = 'nonzéng honnert fënnef a achzeg'
    two_years = '1989. 2011'
    two_years_desired = '1989. 2011' #Should not be picked up as single date, raise exception

    assert date2txt(a, units, tens, scales, months) == a_desired
    assert date2txt(b, units, tens, scales, months) == b_desired
    assert date2txt(c, units, tens, scales, months) == c_desired
    assert date2txt(d, units, tens, scales, months) == d_desired
    with pytest.raises(ValueError) as e_info:
        assert date2txt(two_years, units, tens, scales, months) == two_years_desired

def test_map_number(cardinals, months):
    a = '651'
    a_desired = 'sechs honnert een a fofzeg'
    b = '311000'
    b_desired = "dräi honnert eelef dausend"
    c = '77248931'
    c_desired = 'siwen a siwwenzeg millioun zwee honnert aacht a véierzeg dausend néng honnert een a drësseg'
    d = '1024,876'
    d_desired = 'eendausend véier a zwanzeg komma aacht honnert sechs a siwwenzeg'
    e = '2. Juli 1999'
    e_desired = "zweeten Juli nonzéng honnert néng a nonzeg"
    f = '21.03.2015'
    f_desired = 'een a zwanzegsten Mäerz zweedausend fofzéng'
    g = '15 09 1635'
    g_desired = 'fofzéngten September siechzéng honnert fënnef a drësseg'
    h = "1m10"
    h_desired = "1m10" ## Need to fix this
    i = "tëscht 45 an"
    i_desired = "fënnef a véierzeg"

    units, tens, scales = cardinals
    assert map_number(a, units, tens, scales, months) == a_desired
    assert map_number(b, units, tens, scales, months) == b_desired
    assert map_number(c, units, tens, scales, months) == c_desired
    assert map_number(d, units, tens, scales, months) == d_desired
    assert map_number(e, units, tens, scales, months) == e_desired
    assert map_number(f, units, tens, scales, months) == f_desired
    assert map_number(g, units, tens, scales, months) == g_desired
    assert map_number(i, units, tens, scales, months) == i_desired

# def test_exceptions(cardinals, months):
#     units, tens, scales = cardinals
#
#     two_years = """Gegrennt gouf de Päiperleksgaart 1989. 2011 huet Yolande Coop d'Gestioun iwwerholl."""
#     two_years_desired = """Gegrennt gouf de Päiperleksgaart nonzéng honnert néng a nonzeg. zweedausend eelef huet Yolande Coop d'Gestioun iwwerholl."""
#
#     e = "Noutruff 101 1955"
#     e_desired = False
#     f = "1989. 2011"
#     f_desired = False
#
#     assert map_number(two_years, units, tens, scales, months) == two_years_desired
#     assert True
