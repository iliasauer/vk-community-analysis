__author__ = 'nastya_and_ilya'

import bson
import pprint

pprinter = pprint.PrettyPrinter()
with open("Z:\\Bochenina\\MLsample\\comm_7519_members.bson", "rb") as f:
    bsondata = bson.decode_all(f.read())
    for i, d in enumerate(bsondata):
        if i < 10:
            pprinter.pprint(d)
            raw_input()
            print d['last_name']
            raw_input()

