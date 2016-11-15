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
__POST_COMMENT_SRC_ID_KEY = "from_id"

CLIENT = MongoClient()

###############################################################
# db methods
###############################################################


def create_connection(db_name):
    return CLIENT[db_name]


###############################################################
# db task iterators
###############################################################

def run_for_user(post_task, user_task):
    """Iterate users and run the post_task with the user id and user instance for each user"""
    user_db = create_connection(__USER_DB_NAME)
    for user in user_db[__USER_COLLECTION_NAME].find():
        if user[__USER_ID_KEY]:
            user_id = user[__USER_ID_KEY]
            if user_id not in vect_collector:
                vect_collector[user_id] = Vector()
            post_task(user_id)
            user_task(user_id, user)


def run_for_post(user_id, task):
    """Iterate posts and run the task with the user id and the post instance for each post
    https://vk.com/dev/objects/post"""
    post_db = create_connection(__POST_DB_NAME)
    for post in post_db[__POST_COLLECTION_NAME].find():
        task(user_id, post)

###############################################################
# vector updating
###############################################################


def vectors():
    return vect_collector.values()


def collect_vect_components():
    run_for_user(common_post_task, common_user_task)


###############################################################
# user tasks
###############################################################


def common_post_user_task(user_id):
    return run_for_post(user_id, common_post_task)


def common_user_task(user_id, user):
    vect = vect_collector[user_id]
    __subscribed_user_task(user, vect)
    __followed_user_task(user, vect)


def __subscribed_user_task(user, vector):
    subscribs = user[__USER_SUBSCRIB_KEY]
    vector.subscribed = len(subscribs)


def __followed_user_task(user, vector):
    follows = user[__USER_FOLLOW_KEY]
    vector.followed = len(follows)


###############################################################
# post tasks
###############################################################

def __like_post_task(user_id, post, vector):
    likes = post[__POST_LIKE_KEY]
    if user_id in likes:
        vector.inc_liked()


def __repost_post_task(user_id, post, vector):
    reposts = post[__POST_REPOST_KEY]
    if user_id in reposts:
        vector.inc_reposted()


def __comment_post_task(user_id, post, vector):
    comments = post[__POST_COMMENT_KEY]
    for comment in comments:
        src_id = comment[__POST_COMMENT_SRC_ID_KEY]
        if user_id == src_id:
            vector.inc_commented()


def common_post_task(user_id, post):
        vect = vect_collector[user_id]
        __like_post_task(user_id, post, vect)
        __repost_post_task(user_id, post, vect)
        __comment_post_task(user_id, post, vect)
