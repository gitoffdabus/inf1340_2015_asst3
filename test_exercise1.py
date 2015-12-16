#!/usr/bin/env python
from exercise1 import selection, projection, cross_product

""" Assignment 3, Exercise 1, INF1340, Fall, 2015. DBMS
Test module for exercise3.py

"""

__author__ = 'Oli_Mib_Par'

###########
# TABLES ##
###########

EMPLOYEES = [["Surname", "FirstName", "Age", "Salary"],
             ["Smith", "Mary", 25, 2000],
             ["Black", "Lucy", 40, 3000],
             ["Verdi", "Nico", 36, 4500],
             ["Smith", "Mark", 40, 3900]]

R1 = [["Employee", "Department"],
      ["Smith", "sales"],
      ["Black", "production"],
      ["White", "production"]]

R2 = [["Department", "Head"],
      ["production", "Mory"],
      ["sales", "Brown"]]

R3 = [[]]

R4 = [["A", "B"]]

R5 = [["C", "D"]]

R6 = [["A", "B"], [1, 2], [3, 4]]

R7 = [["C", "D"], [5, 6]]

GRADUATES = [["Number", "Surname", "Age"],
             [7285, "Ryan", 37],
             ["Surname", "Jack", 39],
             [9555, "Darkes", 38]]


#####################
# HELPER FUNCTIONS ##
#####################


def is_equal(t1, t2):
    t1.sort()
    t2.sort()

    return t1 == t2


#####################
# FILTER FUNCTIONS ##
#####################


def filter_employees(row):
    """
    Check if employee represented by row
    is AT LEAST 30 years old and makes
    MORE THAN 3500.
    :param row: A List in the format:
        [{Surname}, {FirstName}, {Age}, {Salary}]
    :return: True if the row satisfies the condition.
    """
    return row[-2] >= 30 and row[-1] > 3500


###################
# TEST FUNCTIONS ##
###################


def test_selection():
    """
    Test select operation.
    """

    result = [["Surname", "FirstName", "Age", "Salary"],
              ["Verdi", "Nico", 36, 4500],
              ["Smith", "Mark", 40, 3900]]
    assert is_equal(result, selection(EMPLOYEES, filter_employees))
    assert selection(GRADUATES, filter_employees) is None
    assert selection(R3, filter_employees) is None


def test_projection():
    """
    Test projection operation.
    """

    result = [["Surname", "FirstName"],
              ["Smith", "Mary"],
              ["Black", "Lucy"],
              ["Verdi", "Nico"],
              ["Smith", "Mark"]]
    result_2 = [["Age", "Salary"],
                [25, 2000],
                [40, 3000],
                [36, 4500],
                [40, 3900]]
    result_3 = [["Surname"],
                ["Smith"],
                ["Black"],
                ["Verdi"],
                ["Smith"]]

    assert is_equal(result, projection(EMPLOYEES, ["Surname", "FirstName"]))
    assert is_equal(result_2, projection(EMPLOYEES, ["Age", "Salary"]))
    assert is_equal(result_3, projection(EMPLOYEES, ["Surname"]))
    try:
        projection(EMPLOYEES, ["inf"])
    except ValueError:
        assert True

    try:
        projection(R3, ["inf"])
    except ValueError:
        assert True

    try:
        projection(R3, [""])
    except ValueError:
        assert True


def test_cross_product():
    """
    Test cross product operation.
    """

    result = [["Employee", "Department", "Department", "Head"],
              ["Smith", "sales", "production", "Mory"],
              ["Smith", "sales", "sales", "Brown"],
              ["Black", "production", "production", "Mory"],
              ["Black", "production", "sales", "Brown"],
              ["White", "production", "production", "Mory"],
              ["White", "production", "sales", "Brown"]]

    result2 = [["A", "B", "C", "D"],
               [1, 2, 5, 6],
               [3, 4, 5, 6]]

    assert is_equal(result, cross_product(R1, R2))
    assert is_equal(result2, cross_product(R6, R7))
    assert cross_product(R4, R5) is None
    assert cross_product(R3, R3) is None
