# -*- coding: utf-8 -*-

"""Lab util"""

import re

class DbHardcodeHandler(object):
    """Class to parse some hardcode"""

    @staticmethod
    def find_first_num(some_string):
        match = re.search('(\d+)', some_string)
        if match:
            return match.group()

    @staticmethod
    def find_comm_id(comm_coll_name):
        return DbHardcodeHandler.find_first_num(comm_coll_name)

    __COMM_COLL_NAME_PREFIX__ = "comm_"
    __COMM_COLL_NAME_SUFFIX__ = "_wall_post"

    @staticmethod
    def build_comm_coll_name(comm_id):
        return "%s%d%s" % (DbHardcodeHandler.__COMM_COLL_NAME_PREFIX__,
                           comm_id,
                           DbHardcodeHandler.__COMM_COLL_NAME_SUFFIX__)