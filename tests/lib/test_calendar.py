import pandas as pd

import lib.calendar


def test_generate_actor_description_line():
    """Return the correct string"""
    actor = pd.Series({'ActorNaam': 'A', 'ActorFractie': 'B'})
    expected = 'A (B)'
    assert lib.calendar._generate_actor_description_line(actor) == expected


def test_generate_actor_description_line_with_no_fraction():
    """Return the correct string with fraction as -"""
    actor = pd.Series({'ActorNaam': 'A', 'ActorFractie': None})
    expected = 'A (onbekend)'
    assert lib.calendar._generate_actor_description_line(actor) == expected


def test_generate_actor_description_line_with_no_name():
    """Return the correct string with name as -"""
    actor = pd.Series({'ActorNaam': None, 'ActorFractie': 'B'})
    expected = 'Onbekend (B)'
    assert lib.calendar._generate_actor_description_line(actor) == expected
