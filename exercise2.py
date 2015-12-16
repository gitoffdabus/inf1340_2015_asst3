#!/usr/bin/env python3

""" Assignment 3, Exercise 2, INF1340, Fall, 2015. Kanadia

Computer-based immigration office for Kanadia

"""

__author__ = 'Susan Sim'
__email__ = "ses@drsusansim.org"
__copyright__ = "2015 Susan Sim"
__license__ = "MIT License"

import re
import datetime
import json

######################
## global constants ##
######################
REQUIRED_FIELDS = ["passport", "first_name", "last_name",
                   "birth_date", "home", "entry_reason", "from"]


######################
## global variables ##
######################
'''
countries:
dictionary mapping country codes (lowercase strings) to dictionaries
containing the following keys:
"code","name","visitor_visa_required",
"transit_visa_required","medical_advisory"
'''
COUNTRIES = None


#####################
# HELPER FUNCTIONS ##
#####################

def valid_passport_format(passport_number):
    """
    Checks whether a passport number is five sets of five alpha-number characters separated by dashes
    :param passport_number: alpha-numeric string
    :return: Boolean; True if the format is valid, False otherwise
    """
    passport_format_regex = re.compile(r"(\w{5}-){4}\w{5}$")
    passport_match = passport_format_regex.match(passport_number)
    if passport_match is None:
        return False
    else:
        return True


def valid_visa_format(visa_code):
    """
    Checks whether a visa code is two groups of five alphanumeric characters
    :param visa_code: alphanumeric string
    :return: Boolean; True if the format is valid, False otherwise

    """

    visa_format_regex = re.compile(r"\w{5}-\w{5}$")
    visa_match = visa_format_regex.match(visa_code)
    if visa_match is None:
        return False
    else:
        return True


def valid_date_format(date_string):
    """
    Checks whether a date has the format YYYY-mm-dd in numbers
    :param date_string: date to be checked
    :return: Boolean True if the format is valid, False otherwise
    """
    date_format_regex = re.compile(r"\d{4}-\d{2}-\d{2}")
    date_match = date_format_regex.match(date_string)
    if date_match is None:
        return False
    else:
        return True


def valid_location(citizen_location, ministry_location):
    if "via" in citizen_location.keys():
        if (citizen_location["via"]["country"]).upper() not in ministry_location.keys():
            return False
    elif (citizen_location["home"]["country"]).upper() not in ministry_location.keys() \
            or citizen_location["from"]["country"].upper() not in ministry_location.keys():
        return False
    else:
        return True


def visa_type(citizen_visa, visit_country):
    if citizen_visa["home"]["country"] in visit_country.keys():
        country_code = citizen_visa["home"]["country"]
        if visit_country[country_code]["visitor_visa_required"] == 0:
            return False
        else:
            return True


def reason_for_entry(citizen_reason, country):
    if citizen_reason["entry_reason"] == "returning":
        return False
    elif citizen_reason["entry_reason"] == "visit":
        # Check whether or not visitor visa required
        visa_required = visa_type(citizen_reason, country)
        if visa_required is False:
            return False
        else:
            return True


def medical_advisory_check(citizen, medical_advisory):
    if "via" in citizen.keys() and citizen["via"]["country"] in medical_advisory.keys():
        if medical_advisory[citizen["via"]["country"]]["medical_advisory"] == "":
            return False
        else:
            return True
    elif citizen["from"]["country"] in medical_advisory.keys():
        if medical_advisory[citizen["from"]["country"]]["medical_advisory"] == "":
            return False
        else:
            return True
    else:
        return False


def visa_duration(date_string):
    """
    Check if date is less than two years ago.
    :param date_string: a date string in format "YYYY-MM-DD"
    :return: True if date is less than two years ago; False otherwise.
    """

    now = datetime.datetime.now()
    two_years_ago = now.replace(year=now.year - 2)
    date = datetime.datetime.strptime(date_string, '%Y-%m-%d')
    return (date - two_years_ago).total_seconds() > 0


################
# MAIN FUNCTION
################
def decide(input_file, countries_file):
    """
    Decides whether a traveller's entry into Kanadia should be accepted

    :param input_file: The name of a JSON formatted file that contains
        cases to decide
    :param countries_file: The name of a JSON formatted file that contains
        country data, such as whether an entry or transit visa is required,
        and whether there is currently a medical advisory
    :return: List of strings. Possible values of strings are:
        "Accept", "Reject", and "Quarantine"
    """

    with open(input_file, "r") as file_reader:
        file_contents = file_reader.read()
        json_citizens = json.loads(file_contents)
    with open(countries_file, "r") as file_reader2:
        file_contents2 = file_reader2.read()
        json_countries = json.loads(file_contents2)
    # print json.dumps(json_citizens, indent=1)

    result_list = []
    for citizen in json_citizens:
        new_list = []
        for entry in REQUIRED_FIELDS:
            # Check whether the required information for an entry record is complete
            if entry in citizen.keys():
                new_list.append(entry)
        if new_list == REQUIRED_FIELDS:
            # check whether the passport no, visa no, date are legal
            passport_number_validity = valid_passport_format(citizen["passport"])
            if passport_number_validity is False:
                result_list.append("Reject")
            else:
                # Check whether the traveller's home country is Kanadia
                if citizen["home"]["country"] == "KAN" or citizen["home"]["country"] == "kan":
                    # Check for medical advisory from returning country
                    quarantine_required = medical_advisory_check(citizen, json_countries)
                    if quarantine_required is False:
                        result_list.append("Accept")
                    else:
                        result_list.append("Quarantine")
                else:
                    if "via" in citizen.keys():
                        location = valid_location(citizen, json_countries)
                        if location is False:
                            result_list.append("Reject")
                        else:
                            # Check for medical advisory for "via" country
                            quarantine_required = medical_advisory_check(citizen, json_countries)
                            if quarantine_required is False:
                                result_list.append("Accept")
                            else:
                                result_list.append("Quarantine")
                    else:
                        # Check for other valid locations
                        location = valid_location(citizen, json_countries)
                        if location is False:
                            result_list.append("Reject")
                        elif location is True:
                            # Check reason for entry
                            reason = reason_for_entry(citizen, json_countries)
                            # If reason is to visit & no visa is required then simply check for medical advisory
                            if reason is False:
                                quarantine_required = medical_advisory_check(citizen, json_countries)
                                if quarantine_required is False:
                                    result_list.append("Accept")
                                else:
                                    result_list.append("Quarantine")
                            else:
                                # If visa is required
                                # Check for valid visa number
                                visa_number_validity = valid_visa_format(citizen["visa"]["code"])
                                if visa_number_validity is False:
                                    result_list.append("Reject")
                                else:
                                    # Check for valid visa date
                                    date_format_validity = valid_date_format(citizen["visa"]["date"])
                                    if date_format_validity is False:
                                        print("dt")
                                        result_list.append("Reject")
                                    else:
                                        # Check for valid visa duration
                                        visa_duration_validity = visa_duration(citizen["visa"]["date"])
                                        if visa_duration_validity is False:
                                            result_list.append("Reject")
                                        else:
                                            # If the previous three checks are cleared, check for medical advisory
                                            quarantine_required = medical_advisory_check(citizen, json_countries)
                                            if quarantine_required is False:
                                                result_list.append("Accept")
                                            else:
                                                result_list.append("Quarantine")
        else:
            result_list.append("Reject")
    return result_list



