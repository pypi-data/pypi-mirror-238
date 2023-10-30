#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -------------------
# @Time    : 2022/2/11 5:50 PM
# @Version : 1.0
# @Author  : lvzhidong
# @For : 
# -------------------


def get_column_letter(col_idx):
    """Convert a column number into a column letter (3 -> 'C')

    Right shift the column col_idx by 26 to find column letters in reverse
    order.  These numbers are 1-based, and can be converted to ASCII
    ordinals by adding 64.

    """
    # these indicies corrospond to A -> ZZZ and include all allowed
    # columns
    if not 1 <= col_idx <= 18278:
        raise ValueError("Invalid column index {0}".format(col_idx))
    letters = []
    while col_idx > 0:
        col_idx, remainder = divmod(col_idx, 26)
        # check for exact division and borrow if needed
        if remainder == 0:
            remainder = 26
            col_idx -= 1
        letters.append(chr(remainder+64))
    return ''.join(reversed(letters))


def get_cell_letter(row, col):
    return '{}{}'.format(get_column_letter(col), row)


class Cell(object):
    def __init__(self, row=None, column=None, value=None):
        self.row = row
        """Row number of this cell (1-based)"""
        self.column = column
        """Column number of this cell (1-based)"""
        # _value is the stored value, while value is the displayed value
        self.value = value

    @property
    def coordinate(self):
        """This cell's coordinate (ex. 'A5')"""
        col = get_column_letter(self.column)
        return "{}{}".format(col, self.row)

    @property
    def col_idx(self):
        """The numerical index of the column"""
        return self.column

    @property
    def column_letter(self):
        return get_column_letter(self.column)

    def __str__(self):
        return self.value
