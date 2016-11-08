# -*- coding: utf-8 -*-

"""Lab util"""

from pymongo import MongoClient
import lab.hardcode_util as hc
from lab.vectors import Vector
from lab.vectors import VectorCollector

vect_collector = VectorCollector()

__ZENIT_DB_NAME = 'zenit_vk_communities'
__SPARTAK_DB_NAME = 'spartak_vk_communities'
__MEMBERS_DB_NAME = 'vk_communities_members'

__MEM_ID_KEY__ = "id"

CLIENT = MongoClient()


def create_connection(db_name):
    return CLIENT[db_name]


def check_coll(db_name, coll_name):
    db = create_connection(db_name)
    if coll_name in db.collection_names():
        return db[coll_name].find()


def try_find_coll(db_names, coll_name):
    for db_name in db_names:
        coll = check_coll(db_name, coll_name)
        if coll:
            return coll


def run_for_member(task, limit=-1):
    """Iterate members and run the task with the member id
    and the name of a collection that the member from for each member"""

    mem_db = create_connection(__MEMBERS_DB_NAME)  # get db
    for mem_coll_name in mem_db.collection_names():  # for each collection in db
        for entry in mem_db[mem_coll_name].find():  # for each member in collection
            if entry[__MEM_ID_KEY__]:  # if member has id
                mem_id = entry[__MEM_ID_KEY__]  # get id
                vect_collector.put(mem_id, Vector())  # create new vector for member
                comm_coll_name = hc.mem_coll_name_to_comm_coll_name(mem_coll_name)
                # determine the name of a community the member from
                task(mem_id, comm_coll_name)
                # run task with the member id and the community name
                limit -= 1
                if limit is 0:
                    return


def print_task(descript, some_val):
    print("%s: %s" % (descript, str(some_val)))

def run_for_post(mem_id, comm_coll_name, task, limit=-1):
    """Iterate posts and run the task with the member id
    and the post entry for each post
    https://vk.com/dev/objects/post"""

    db_names = [__ZENIT_DB_NAME, __SPARTAK_DB_NAME]  # set names of dbs
    comm = try_find_coll(db_names, comm_coll_name)  # try to find the community in dbs by name
    if comm:  # if found
        for post in comm:  # for each post in the community
            task(mem_id, post)  # run task with the member id and the post entry
            limit -= 1
            if limit is 0:
                return

# TODO user handling
# def find_liking_users(post):


# def run_for_user(mem_id, post, find_users_task, task, limit=-1):  # user is a member that make some action
#     """Iterate users and run the task with *** for each user"""


def print_post_owner_id_for_post_task(mem_id, comm_coll_name, limit=-1):
    return run_for_post(mem_id, comm_coll_name,
                        print_post_from_id, limit)


def print_post_from_id(mem_id, post):
    post_data = post["post_data"]
    from_id = post_data["from_id"] # идентификатор автора записи
    if from_id < 0:
        from_id = - from_id
    vect = vect_collector.get(mem_id)
    if mem_id == from_id:
        vect.created += 1
        print("STOPPED. SUCCESS.")
        return
    print("mem id: %s; from id: %s" % (mem_id, from_id))
    print("mem id %s vector: %s" % (mem_id, vect))
