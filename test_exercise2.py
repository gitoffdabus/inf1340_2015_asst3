#!/usr/bin/env python3
# imports one per line
import os
from exercise2 import decide
""" Module to test papers.py  """

__author__ = 'Mib_Oli_Par'


DIR = "test_jsons/"
os.chdir(DIR)


def test_returning():
    """
    Travellers are returning to KAN.
    """
    assert decide("test_returning_citizen.json", "countries.json") ==\
        ["Accept", "Accept", "Quarantine"]


def test_unknown_location():
    """
    Travellers with unknown location
    #1 Both the locations are unknown - home & from
    #2 Only one location is unknown
    :return:
    """

    assert decide("unknown_location.json", "countries.json") ==\
        ["Reject", "Reject"]


def test_visa_validity():
    """
    Travellers requiring Visa will need a validity check
    #1 Traveller requires valid visa
    #2 Invalid date format
    #3 Invalid visa code format
    #4 Traveler requires a visa but his validity is over
    """
    assert decide("visa_validity.json", "countries.json") ==\
        ["Accept", "Reject", "Reject", "Reject"]


def test_medical_advisory():
    """
    Test for travelers traveling from
    countries having medical advisories
    #1 Traveler belonging to Kanadia but
    traveling from a country having medical advisory
    #2 Traveler from some other country,
    traveling from a country having medical advisory
    """

    assert decide("medical_advisory.json", "countries.json") ==\
        ["Quarantine", "Quarantine"]


def test_miscellaneous():
    """
    Tests for some minor details in traveler's data
    #1 Whether all the required fields are provided or nor (last name missing)
    #2 Lowercase passport numbers
    #3 Lowercase country code
    #4 Whether the passport number is in correct format
    #5 If the traveler is traveling via a country having medical advisory
    """

    assert decide("miscellaneous.json", "countries.json") ==\
        ["Reject", "Accept", "Accept", "Reject", "Quarantine"]
