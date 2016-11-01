# -*- coding: utf-8 -*-

"""Lab util"""

import re
from pymongo import MongoClient


class DbHardcodeHandler(object):
    """Class to parse some hardcode"""

    __COMM_COLL_NAME_PREFIX__ = "comm_"
    __COMM_COLL_NAME_SUFFIX__ = "_wall_post"
    __MEMB_COLL_NAME_PREFIX__ = __COMM_COLL_NAME_PREFIX__
    __MEMB_COLL_NAME_SUFFIX__ = "_members"

    @staticmethod
    def find_first_num(some_string):
        match = re.search('(\d+)', some_string)
        if match:
            return match.group()

    @staticmethod
    def find_comm_id(comm_coll_name):
        return DbHardcodeHandler.find_first_num(comm_coll_name)

    @staticmethod
    def __build_coll_name(prefix, comm_id, suffix):
        return "%s%d%s" % (prefix, comm_id, suffix)

    @staticmethod
    def build_comm_coll_name(comm_id):
        return DbHardcodeHandler.__build_coll_name(
            DbHardcodeHandler.__COMM_COLL_NAME_PREFIX__,
            comm_id,
            DbHardcodeHandler.__COMM_COLL_NAME_SUFFIX__
        )

    @staticmethod
    def build_memb_coll_name(comm_id):
        return DbHardcodeHandler.__build_coll_name(
            DbHardcodeHandler.__MEMB_COLL_NAME_PREFIX__,
            comm_id,
            DbHardcodeHandler.__MEMB_COLL_NAME_SUFFIX__
        )


class DbMiner(object):
    """Class to parse some hardcode"""

    __ZENIT_DB_NAME__ = 'zenit_vk_communities'
    __SPARTAK_DB_NAME__ = 'spartak_vk_communities'
    __MEMBERS_DB_NAME__ = 'vk_communities_members'

    __MEM_ID_KEY__ = "id"

    CLIENT = MongoClient()
    # ZENIT_DB = CLIENT[ZENIT_DB_NAME]
    # SPARTAK_DB = CLIENT[SPARTAK_DB_NAME]
    # MEMBERS_DB = CLIENT[MEMBERS_DB_NAME]

    @staticmethod
    def create_connection(db_name):
        return DbMiner.CLIENT[db_name]

    def run_for_mem_id(self, task, limit=-1):
        mem_db = self.create_connection(DbMiner.__MEMBERS_DB_NAME__)
        for coll_name in mem_db.collection_names():
            for entry in mem_db[coll_name].find():
                if entry[DbMiner.__MEM_ID_KEY__]:
                    mem_id = entry[DbMiner.__MEM_ID_KEY__]
                    task(DbMiner.__MEM_ID_KEY__, mem_id)
                    limit -= 1
                    if limit is 0:
                        return

    @staticmethod
    def print_task(descript, some_val):
        print("%s: %s" % (descript, str(some_val)))

    #
    # POST_ID_DESIGN = "_id"
    #
    # counter = 0
    # for coll_name in MEMBERS_DB.collection_names():
    #     for post in MEMBERS_DB[coll_name].find():
    #         if post[POST_ID_DESIGN]:
    #             counter += 1
    #
    # print("Number of members: %d" % counter)
