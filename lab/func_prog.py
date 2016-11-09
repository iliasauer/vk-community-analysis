# -*- coding: utf-8 -*-

"""Functional programming util"""


def task_with_check(predicate, predicate_args, task):
    if predicate(predicate_args[0], predicate_args[1]):
        task()
