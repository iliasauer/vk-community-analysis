# -*- coding: utf-8 -*-

"""Math util"""


def mod_eq(num1, num2):
    if num1 > num2:
        return not bool(num1 % num2)
    else:
        return not bool(num2 % num1)
