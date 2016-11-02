# -*- coding: utf-8 -*-

"""Lab util"""

import re
from pymongo import MongoClient


class DbHardcodeHandler(object):
    """Class to parse some hardcode"""

    __COMM_COLL_NAME_PREFIX = "comm_"
    __COMM_COLL_NAME_SUFFIX = "_wall_post"
    __MEMB_COLL_NAME_PREFIX = __COMM_COLL_NAME_PREFIX
    __MEMB_COLL_NAME_SUFFIX = "_members"

    @staticmethod
    def find_first_num(some_string):
        match = re.search('(\d+)', some_string)
        if match:
            return match.group()

    @staticmethod
    def find_comm_id(coll_name):
        return DbHardcodeHandler.find_first_num(coll_name)

    @staticmethod
    def __build_coll_name(prefix, comm_id, suffix):
        return "%s%d%s" % (prefix, comm_id, suffix)

    @staticmethod
    def build_comm_coll_name(comm_id):
        return DbHardcodeHandler.__build_coll_name(
            DbHardcodeHandler.__COMM_COLL_NAME_PREFIX,
            comm_id,
            DbHardcodeHandler.__COMM_COLL_NAME_SUFFIX
        )

    @staticmethod
    def build_mem_coll_name(comm_id):
        return DbHardcodeHandler.__build_coll_name(
            DbHardcodeHandler.__MEMB_COLL_NAME_PREFIX,
            comm_id,
            DbHardcodeHandler.__MEMB_COLL_NAME_SUFFIX
        )

    @staticmethod
    def comm_coll_name_to_mem_coll_name(comm_coll_name):
        comm_id = DbHardcodeHandler.find_comm_id(comm_coll_name)
        return DbHardcodeHandler.build_mem_coll_name(comm_id)

    @staticmethod
    def mem_coll_name_to_comm_coll_name(mem_coll_name):
        comm_id = DbHardcodeHandler.find_comm_id(mem_coll_name)
        return DbHardcodeHandler.build_comm_coll_name(comm_id)


class DbMiner(object):
    """Class to parse some hardcode"""

    __ZENIT_DB_NAME = 'zenit_vk_communities'
    __SPARTAK_DB_NAME = 'spartak_vk_communities'
    __MEMBERS_DB_NAME = 'vk_communities_members'

    __MEM_ID_KEY__ = "id"

    CLIENT = MongoClient()

    @staticmethod
    def create_connection(db_name):
        return DbMiner.CLIENT[db_name]

    @staticmethod
    def check_coll(db_name, coll_name):
        db = DbMiner.create_connection(db_name)
        if coll_name in db.collection_names():
            return db[coll_name].find()

    @staticmethod
    def try_find_coll(db_names, coll_name):
        for db_name in db_names:
            coll = DbMiner.check_coll(db_name, coll_name)
            if coll:
                return coll

    @staticmethod
    def run_for_mem_id(task, limit=-1):
        mem_db = DbMiner.create_connection(DbMiner.__MEMBERS_DB_NAME)
        for mem_coll_name in mem_db.collection_names():
            for entry in mem_db[mem_coll_name].find():
                if entry[DbMiner.__MEM_ID_KEY__]:
                    mem_id = entry[DbMiner.__MEM_ID_KEY__]
                    comm_coll_name = DbHardcodeHandler.mem_coll_name_to_comm_coll_name(mem_coll_name)
                    task(DbMiner.__MEM_ID_KEY__, mem_id, mem_coll_name, comm_coll_name)
                    limit -= 1
                    if limit is 0:
                        return

    @staticmethod
    def print_task(descript, some_val):
        print("%s: %s" % (descript, str(some_val)))

    @staticmethod
    def run_for_coll_task(comm_coll_name, task, limit=-1):
        db_names = [DbMiner.__ZENIT_DB_NAME, DbMiner.__SPARTAK_DB_NAME]
        coll = DbMiner.try_find_coll(db_names, comm_coll_name)
        if coll:
            for entry in coll:
                task(entry)
                limit -= 1
                if limit is 0:
                    return





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
