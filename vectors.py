#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Vectors collecting"""

from pymongo import MongoClient
from lab_util import DbHardcodeHandler as Hardcode


ZENIT_DB_NAME = 'zenit_vk_communities'
SPARTAK_DB_NAME = 'spartak_vk_communities'
MEMBERS_DB_NAME = 'vk_communities_members'

CLIENT = MongoClient()
ZENIT_DB = CLIENT[ZENIT_DB_NAME]
SPARTAK_DB = CLIENT[SPARTAK_DB_NAME]
MEMBERS_DB = CLIENT[MEMBERS_DB_NAME]

POST_ID_DESIGN = "_id"

counter = 0
for coll_name in MEMBERS_DB.collection_names():
    for post in MEMBERS_DB[coll_name].find():
        if post[POST_ID_DESIGN]:
            counter += 1

print("Number of members: %d" % counter)
