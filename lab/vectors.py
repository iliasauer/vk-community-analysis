# -*- coding: utf-8 -*-

"""Vectors"""

# noinspection PyAttributeOutsideInit
class Vector(object):
    """Vector structure"""

    def __init__(self):
        # self.__id = mem_id
        self.__created = 0
        self.__liked = 0
        self.__commented = 0
        self.__reposted = 0
        self.__subscribed = 0
        self.__followed = 0

    def inc_created(self):
        self.__created += 1

    def inc_liked(self):
        self.__liked += 1

    def inc_commented(self):
        self.__commented += 1

    def inc_reposted(self):
        self.__reposted += 1

    def inc_subscribed(self):
        self.__subscribed += 1

    def inc_followed(self):
        self.__followed += 1

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s" % (self.__created, self.__liked, self.__commented,
                                           self.__reposted, self.__subscribed, self.__followed)


class VectorCollector(object):
    """Class to collect vectors"""
    def __init__(self):
        self.__vect_dict = {}

    def put(self, mem_id, vector):
        self.__vect_dict[mem_id] = vector

    def get(self, mem_id):
        return self.__vect_dict.get(mem_id, 0)

    def __str__(self):
        return str(self.__vect_dict)
