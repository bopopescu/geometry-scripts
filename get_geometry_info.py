import os
import sys
import operator
import cdb
from cdb import Geometry
import subprocess

### PUBLIC SLAVE = "http://cdb.mice.rl.ac.uk"
### PREPROD = "http://preprodcdb.mice.rl.ac.uk"

_R_SERVER = None
_serverType = None

#############################################################
class GeometryHelper:

    def __init__(self):
        self._tstart = '2015-01-01 00:00:00'
        self._tend = '2018-12-31 00:00:00'

        self.downloadServer = None
        if _serverType == "preprod":
            _R_SERVER = "http://preprodcdb.mice.rl.ac.uk:8080"
            self.downloadServer = _R_SERVER + "/cdb/"
        elif _serverType == "prod":
            _R_SERVER = "http://cdb.mice.rl.ac.uk/"
            self.downloadServer = _R_SERVER + "/cdb/"

        self.server = Geometry(_R_SERVER)

#########################################
    def get_ids(self):
        ids = self.server.get_ids(self._tstart, self._tend)
        print type(ids)
        print ids
        for idnum, geom in ids.iteritems():
            print '===== ID: ',idnum
            if idnum < 120:
                continue
            print 'CREATED ON: ',geom['created']
            print 'VALID FROM: ',geom['validFrom']
            print geom['notes']
        return ids
#########################################
    def get_latest_ids(self):
        ids = self.server.get_ids(self._tstart, self._tend)
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
            print 'VALID_FROM: ', t[0], 'HighestID: ',slist[0][0], 'CREATED: ',slist[0][1]
            print
#########################################
    def get_geometries(self, ids):
        pwd = os.environ['PWD']
        for idnum, geom in ids.iteritems():
            if idnum < 120:
                continue
            print '+++ Getting geometry for ID: ',idnum
            id_dir = 'geo-'+str(idnum)
            if _serverType == "preprod":
                geoDir = os.path.join(pwd,'preprodgeo',id_dir)
            elif _serverType == "prod":
                geoDir = os.path.join(pwd,'prodgeo',id_dir)
            if not os.path.isdir(geoDir):
                os.system('mkdir %s' % geoDir)
                GEO_EXE = os.path.join(os.environ['MAUS_ROOT_DIR'],'bin/utilities/download_geometry.py')
                geo_cmd = [ GEO_EXE, '-geometry_download_by', 'id', '-geometry_download_id', str(idnum), '-geometry_download_directory', geoDir, '-cdb_download_url', self.downloadServer]
                subprocess.call(geo_cmd)

#########################################
    def get_corrections(self, runMin, runMax):
        old_corr = None
        for run in range(runMin, runMax): 
            try:
                this_corr = self.server.get_corrections_for_run_xml(run) 
                if this_corr != old_corr:
                    print
                    print '>>> Correction for Run# ', run, ' has changed'
                    print this_corr
                    old_corr = this_corr
            except cdb._exceptions.CdbPermanentError:
                pass
            
#           else:
#               print this_corr
#               print '++ ',run
#               print old_corr
#               print
    
#############################################################
if __name__ == "__main__":
   try:
       _serverType = sys.argv[1]
       _downloadType = sys.argv[2]
   except Exception as e:
       print e
   if _serverType != "preprod" and _serverType != "prod":
       print "Invalid server type: ", _serverType, " : must be prod or preprod"
       exit
   if _downloadType != "check" and _serverType != "download":
       print "Invalid download type: ", _downloadType, " : must be check or download"
       exit
   
   geoHelper = GeometryHelper()
   ids = geoHelper.get_ids()
   #ids = geoHelper.get_latest_ids()
   if _downloadType == "download":
       geoHelper.get_geometries(ids)
#  geoHelper.get_corrections(8400, 10015)
