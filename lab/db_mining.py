# -*- coding: utf-8 -*-

"""Database mining"""

from pymongo import MongoClient
import lab.hardcode_util as hc
import lab.math as math
import lab.vectors as vctrs
import lab.func_prog as fp
from lab.vectors import Vector
from lab.vectors import VectorCollector

vect_collector = VectorCollector()

__ZENIT_DB_NAME = 'zenit_vk_communities'
__SPARTAK_DB_NAME = 'spartak_vk_communities'
__MEMBERS_DB_NAME = 'vk_communities_members'

__MEM_ID_KEY = "id"
__POST_COMMENTS_KEY = "comments"
__POST_INFO_KEY = "post_data"
__SRC_ID_KEY = "from_id"

CLIENT = MongoClient()

###############################################################
# db methods
###############################################################


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


###############################################################
# db entities task iterators
###############################################################

def run_for_member(task, limit=-1):
    """Iterate members and run the task with the member id
    and the name of a collection that the member from for each member"""

    mem_db = create_connection(__MEMBERS_DB_NAME)  # get db
    for mem_coll_name in mem_db.collection_names():  # for each collection in db
        print("Member collection name: %s" % mem_coll_name)
        for entry in mem_db[mem_coll_name].find():  # for each member in collection
            if entry[__MEM_ID_KEY]:  # if member has id
                mem_id = entry[__MEM_ID_KEY]  # get id
                if not bool(vect_collector.get(mem_id)):
                    vect_collector.put(mem_id, Vector())  # create new vector for member
                comm_coll_name = hc.mem_coll_name_to_comm_coll_name(mem_coll_name)
                # determine the name of a community the member from
                task(mem_id, comm_coll_name)
                # run task with the member id and the community name
                limit -= 1
                if limit is 0:
                    return


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


###############################################################
# vector updating
###############################################################


def update_vector(mem_id, src_id, update_task):
    vect = vect_collector.get(mem_id)
    update_task(mem_id, src_id, vect)
    print("mem id: %s; from id: %s" % (mem_id, src_id))
    print("mem id %s vector: %s" % (mem_id, vect))


def check_authorship(mem_id, src_id):
    return math.mod_eq(mem_id, src_id)


def check_and_change_vect_component(mem_id, src_id, change_task):
    check_args = (mem_id, src_id)
    fp.task_with_check(check_authorship, check_args, change_task)


def check_and_inc_commented_prop(mem_id, src_id, vect):
    check_and_change_vect_component(mem_id, src_id, vect.inc_commented)


def check_and_inc_created_prop(mem_id, src_id, vect):
    check_and_change_vect_component(mem_id, src_id, vect.inc_created)


###############################################################
# member tasks
###############################################################


def create_post_member_task(mem_id, comm_coll_name, limit=-1):
    print("Community collection name: %s" % comm_coll_name)
    return run_for_post(mem_id, comm_coll_name, create_post_task, limit)


def comment_post_member_task(mem_id, comm_coll_name, limit=-1):
    return run_for_post(mem_id, comm_coll_name, comment_post_task, limit)


###############################################################
# post tasks
###############################################################


def create_post_task(mem_id, post):
    post_data = post["post_data"]
    update_vector(mem_id, post_data[__SRC_ID_KEY], check_and_inc_created_prop)


def comment_post_task(mem_id, post):
    comments = post["comments"]
    if comments:
        for comment in comments:
            update_vector(mem_id, comment["from_id"], check_and_inc_commented_prop)
