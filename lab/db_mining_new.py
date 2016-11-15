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

def run_for_user(task):
    """Iterate users and run the task with the user id and user instance for each user"""
    user_db = create_connection(__USER_DB_NAME)
    for user in user_db[__USER_COLLECTION_NAME].find():
        if user[__USER_ID_KEY]:
            user_id = user[__USER_ID_KEY]
            if user_id not in vect_collector:
                vect_collector[user_id] = Vector()
            task(user_id, user)


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
    vect_collector.values()


def collect_all():
    collect_likes()
    collect_reposts()
    collect_comments()
    collect_subscriptions()
    collect_followers()


def collect_likes():
    run_for_user(like_post_user_task)


def collect_reposts():
    run_for_user(repost_post_user_task)


def collect_comments():
    run_for_user(comment_post_user_task)


def collect_subscriptions():
    run_for_user(subscribed_user_task)


def collect_followers():
    run_for_user(followed_user_task)


###############################################################
# user tasks
###############################################################


def like_post_user_task(user_id):
    return run_for_post(user_id, __like_post_task)


def repost_post_user_task(user_id):
    return run_for_post(user_id, __repost_post_task)


def comment_post_user_task(user_id):
    return run_for_post(user_id, __comment_post_task)


def subscribed_user_task(user_id, user):
    subscribs = user[__USER_SUBSCRIB_KEY]
    vect = vect_collector[user_id]
    vect.subscribed = len(subscribs)


def followed_user_task(user_id, user):
    follows = user[__USER_FOLLOW_KEY]
    vect = vect_collector[user_id]
    vect.followed = len(follows)


###############################################################
# post tasks
###############################################################

def __like_post_task(user_id, post):
    likes = post[__POST_LIKE_KEY]
    if user_id in likes:
        vect = vect_collector[user_id]
        vect.inc_liked()


def __repost_post_task(user_id, post):
    reposts = post[__POST_REPOST_KEY]
    if user_id in reposts:
        vect = vect_collector[user_id]
        vect.inc_reposted()


def __comment_post_task(user_id, post):
    comments = post[__POST_COMMENT_KEY]
    for comment in comments:
        src_id = comment[__POST_COMMENT_SRC_ID_KEY]
        if src_id == user_id:
            vect = vect_collector[user_id]
            vect.inc_commented()
