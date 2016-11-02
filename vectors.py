# -*- coding: utf-8 -*-

"""Vectors util"""


# noinspection PyAttributeOutsideInit
class Vector(object):
    """Vector structure"""

    def __init__(self, mem_id):
        self.__id = mem_id
        self.__created = 0
        self.__liked = 0
        self.__commented = 0
        self.__reposted = 0
        self.__subscribed = 0
        self.__followed = 0

    @property
    def id(self):
        return self.__id

    @property
    def created(self):
        return self.__created

    @created.setter
    def created(self, value):
        self.__created = value

    @property
    def liked(self):
        return self.__liked

    @liked.setter
    def liked(self, value):
        self.__liked = value

    @property
    def commented(self):
        return self.__commented

    @commented.setter
    def commented(self, value):
        self.__commented = value

    @property
    def reposted(self):
        return self.__reposted

    @reposted.setter
    def reposted(self, value):
        self.__reposted = value

    @property
    def subscribed(self):
        return self.__subscribed

    @subscribed.setter
    def subscribed(self, value):
        self.__subscribed = value

    @property
    def followed(self):
        return self.__followed

    @followed.setter
    def followed(self, value):
        self.__followed = value

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s" % (self.__created, self.__liked, self.__commented,
                                           self.__reposted, self.__subscribed, self.__followed)


class VectorCollector(object):
    """Class to collect vectors"""
    def __init__(self, vect_dict):
        self.__vect_dict = {}

    def put(self, mem_id, vector):
        self.__vect_dict[mem_id] = vector

    def get(self, mem_id):
        return self.__vect_dict[mem_id]

    def __str__(self):
        return str(self.__vect_dict)
