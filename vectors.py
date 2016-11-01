#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Vectors collecting"""


from lab_util import DbHardcodeHandler as Hardcode
from lab_util import DbMiner as Miner

MINER = Miner()
MINER.run_for_mem_id(MINER.print_task, 10)
