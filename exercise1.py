#!/usr/bin/env python3

""" Assignment 3, Exercise 2, INF1340, Fall, 2015. DBMS

This module performs table operations on database tables
implemented as lists of lists. """

__author__ = 'Oli_Mib_Par'

#####################
# HELPER FUNCTIONS ##
#####################

def remove_duplicates(l):
    """
    Removes duplicates from l, where l is a List of Lists.
    :param l: a List
    """

    d = {}
    result = []
    for row in l:
        if tuple(row) not in d:
            result.append(row)
            d[tuple(row)] = True

    return result


class UnknownAttributeException(Exception):
    """
    Raised when attempting set operations on a table
    that does not contain the named attribute
    """
    pass


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


def selection(t, f):
    """
    Performs selection operation on table t that satisfies condition f.
    :param: t - a table
    :param: f - a function which is to be applied to t
    :returns: a table, which results from applying function f to table t.
              If result is an empty table the function returns None.

    Example:
    > R = [["A", "B", "C"], [1, 2, 3], [4, 5, 6]]
    ># Define function f that returns True iff
    > # the last element in the row is greater than 3.
    > def f(row): row[-1] > 3
    > select(R, f)
    [["A", "B", "C"], [4, 5, 6]]

    """
    i = 0
    table = [] #resulting table
    flag1 = False #check for function return
    flag2 = False #check if result is populated

    # return None if table to run function is empty
    if t == None:
        return None

    for row in t:
        if i == 0:
            table.append(row) #add the first row of labels
        else:
            flag1 = f(row)
            if flag1:
                table.append(row)
                flag2 = True #atleast one row matches the function
            else:
                continue
        i = i+1

    if flag2:
        return table
    else:
        return None


def index_calculator(row, r):
    """ Stores the index of the matching columns in a new list
    :param: row - the row of the table in which the attribute is to be found
    :param: r - the attributes subset
    :returns: a list which contains the indexes of the attributes
    """

    new_list = []
    for index in r:
        if index in row:
            # if element exists in the table, add to table as an index number
            new_list.append(row.index(index))
    # sort the index number
    new_list.sort()
    return new_list


def projection(t, r):
    """
    Perform projection operation on table t using the attributes subset r.
    :param: a table in which the attributes are to be found
    :param: an attribute subset
    :return: the resulting table containing the entities
    Example:
    > R = [["A", "B", "C"], [1, 2, 3], [4, 5, 6]]
    > projection(R, ["A", "C"])
    [["A", "C"], [1, 3], [4, 6]]

    """

    # call helper to get index of matching columns
    attribute_index = index_calculator(t[0], r)
    print (attribute_index)
    if attribute_index is []:
        # Raise exception if there is no matching attribute
        raise UnknownAttributeException
    else:
        result_table = []
        temp_list = []
        for row in t:
            for index in attribute_index:
                temp_list.append(row[index])
            result_table.append(temp_list)
            temp_list = []
    return result_table


def cross_product(t1, t2):
    """
    Preforms the cross-product of two tables
    :param: two tables t1 & t2
    :return: the cross-product of tables t1 and t2.

    Example:
    > R1 = [["A", "B"], [1,2], [3,4]]
    > R2 = [["C", "D"], [5,6]]
    [["A", "B", "C", "D"], [1, 2, 5, 6], [3, 4, 5, 6]]


    """
    if t1 is None or t2 is None:
        return None
    else:
        result_table = [t1[0] + t2[0]]
        for row1 in t1[1:]:
            for row2 in t2[1:]:
                temp_list = row1 + row2
                result_table.append(temp_list)
    if len(result_table) <= 1:
        result = None
        return result
    else:
        return result_table


