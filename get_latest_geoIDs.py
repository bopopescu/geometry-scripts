"""
Script to get a list of geometry IDs in a given time range
And:
    for every valid_from date, list the highest ID (~~ latest created) in the database

_tstart and _tend control the start and end time within which to query for IDs
"""

import sys
import os
import operator
import cdb
_server = "http://cdb.mice.rl.ac.uk"
_tstart = '2014-01-01 00:00:00'
_tend = '2018-09-01 00:00:00'

def get_geo_ids():
    geo = cdb.Geometry(_server)

    ids = geo.get_ids(_tstart, _tend)

    # ids is a dict
    # key = id
    # value = dict
    vdict = {}
    for k, v in ids.iteritems():
        idlist = []
        vali = v['validFrom']
        creat = v['created']
        this_id = k
        idlist.append(this_id)
        idlist.append(creat)
        if not vali in vdict:
            vdict[vali] = []
        vdict[vali].append(idlist)

    for t in sorted(vdict.items(), key=lambda x: x[0]):
        slist = sorted(t[1], key=operator.itemgetter(0), reverse=True)
        print 'For this date: ', t[0], 'the highest ID is ',slist[0][0], 'created on: ',slist[0][1]
        print

get_geo_ids()
