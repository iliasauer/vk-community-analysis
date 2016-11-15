# -*- coding: utf-8 -*-

"""Vectors"""


# noinspection PyAttributeOutsideInit
class Vector(object):
    """Vector structure"""

    def __init__(self):
        # self.__id = mem_id
        # self.__participated = 0
        self.__liked = 0
        self.__reposted = 0
        self.__commented = 0
        self.__subscribed = 0
        self.__followed = 0

    # def inc_participated(self):
    #     self.__participated += 1

    def inc_liked(self):
        self.__liked += 1

    def inc_reposted(self):
        self.__reposted += 1

    def inc_commented(self):
        self.__commented += 1

    # @property
    # def participated(self):
    #     return self.__participated

    @property
    def liked(self):
        return self.__liked

    @property
    def reposted(self):
        return self.__reposted

    @property
    def commented(self):
        return self.__commented

    @property
    def followed(self):
        return self.__followed

    @followed.setter
    def followed(self, followed):
        self.__followed = followed

    @property
    def subscribed(self):
        return self.__subscribed

    @subscribed.setter
    def subscribed(self, subscribed):
        self.__subscribed = subscribed

    def __str__(self):
        return "%s, %s, %s, %s, %s" % (self.__liked, self.__commented, self.__reposted,
                                       self.__subscribed, self.__followed)


class VectorCollector(object):
    """Class to collect vectors"""
    def __init__(self):
        self.__vect_dict = {}

    def put(self, user_id, vector):
        self.__vect_dict[user_id] = vector

    def get(self, user_id):
        return self.__vect_dict.get(user_id, 0)

    def __str__(self):
        return str(self.__vect_dict)
