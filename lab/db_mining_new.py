# -*- coding: utf-8 -*-

"""Database mining"""

from pymongo import MongoClient
import lab.vectors as vctrs
from lab.vectors import Vector

vect_collector = {}

__POST_DB_NAME = "vk_posts"
__POST_COLLECTION_NAME = "posts"
__USER_DB_NAME = "vk_users"
__USER_COLLECTION_NAME = "users"

__USER_ID_KEY = "id"
__USER_SUBSCRIB_KEY = "subscription_groups_ids"
__USER_FOLLOW_KEY = "subscription_users_ids"
__POST_LIKE_KEY = "likes"
__POST_REPOST_KEY = "reposts"
__POST_COMMENT_KEY = "comments"
__POST_SRC_ID_KEY = "from_id"

CLIENT = MongoClient()


###############################################################
# db methods
###############################################################


def create_connection(db_name):
    return CLIENT[db_name]


###############################################################
# db task iterators
###############################################################

def run_for_user(user_task):
    """Iterate users and run the post_task with the user id and user instance for each user"""
    user_db = create_connection(__USER_DB_NAME)
    for user in user_db[__USER_COLLECTION_NAME].find(no_cursor_timeout=True):
        if user[__USER_ID_KEY]:
            user_id = user[__USER_ID_KEY]
            if user_id not in vect_collector:
                vect_collector[user_id] = Vector()
            user_task(user_id, user)
            # print(vect_collector[user_id])


def run_for_post(task):
    """Iterate posts and run the task with the user id and the post instance for each post
    https://vk.com/dev/objects/post"""
    post_db = create_connection(__POST_DB_NAME)
    for post in post_db[__POST_COLLECTION_NAME].find(no_cursor_timeout=True):
        task(post)


###############################################################
# vector updating
###############################################################


def vectors():
    return vect_collector.values()


def print_vectors():
    for vector in vectors():
        print(vector)


def write_vectors():
    with open('vectors.csv', 'w') as f:
        for vector in vectors():
            f.write("%s\n" % vector.__str__())


def collect_vect_components():
    run_for_user(common_user_task)
    run_for_post(common_post_task)


###############################################################
# user tasks
###############################################################


def common_user_task(user_id, user):
    vect = vect_collector[user_id]
    __subscribed_user_task(user, vect)
    __followed_user_task(user, vect)


def __subscribed_user_task(user, vector):
    subscribs = user.get(__USER_SUBSCRIB_KEY, None)
    if subscribs:
        vector.subscribed = len(subscribs)


def __followed_user_task(user, vector):
    follows = user.get(__USER_FOLLOW_KEY, None)
    if follows:
        vector.followed = len(follows)


###############################################################
# post tasks
###############################################################

def __like_post_task(post):
    likes = post.get(__POST_LIKE_KEY, None)
    if likes:
        for like in likes:
            vect = vect_collector.get(like, None)
            if vect:
                vect.inc_liked()


def __repost_post_task(post):
    reposts = post.get(__POST_REPOST_KEY, None)
    if reposts:
        for repost in reposts:
            src_id = repost[__POST_SRC_ID_KEY]
            vect = vect_collector.get(src_id, None)
            if vect:
                vect.inc_reposted()


def __comment_post_task(post):
    comments = post.get(__POST_COMMENT_KEY, None)
    if comments:
        for comment in comments:
            src_id = comment[__POST_SRC_ID_KEY]
            vect = vect_collector.get(src_id, None)
            if vect:
                vect.inc_commented()


def common_post_task(post):
    __like_post_task(post)
    __repost_post_task(post)
    __comment_post_task(post)
