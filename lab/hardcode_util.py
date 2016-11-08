# -*- coding: utf-8 -*-

"""Lab util"""

import re

__COMM_COLL_NAME_PREFIX = "comm_"
__COMM_COLL_NAME_SUFFIX = "_wall_posts"
__MEMB_COLL_NAME_PREFIX = __COMM_COLL_NAME_PREFIX
__MEMB_COLL_NAME_SUFFIX = "_members"


def find_first_num(some_string):
    match = re.search('(\d+)', some_string)
    if match:
        return match.group()


def find_comm_id(coll_name):
    return find_first_num(coll_name)


def __build_coll_name(prefix, comm_id, suffix):
    return "%s%s%s" % (prefix, str(comm_id), suffix)


def build_comm_coll_name(comm_id):
    return __build_coll_name(
        __COMM_COLL_NAME_PREFIX,
        comm_id,
        __COMM_COLL_NAME_SUFFIX
    )


def build_mem_coll_name(comm_id):
    return __build_coll_name(
        __MEMB_COLL_NAME_PREFIX,
        comm_id,
        __MEMB_COLL_NAME_SUFFIX
    )


def comm_coll_name_to_mem_coll_name(comm_coll_name):
    comm_id = find_comm_id(comm_coll_name)
    return build_mem_coll_name(comm_id)


def mem_coll_name_to_comm_coll_name(mem_coll_name):
    comm_id = find_comm_id(mem_coll_name)
    return build_comm_coll_name(comm_id)
