#!/usr/bin/env python

import os
import sys
import glob
import operator
import ConfigParser
import subprocess
import getopt

from datetime import datetime
from time import strftime, gmtime



fullBackupPrefix = "FULL"
diffBackupPrefix = "DIFF"

p7zCommand = "/usr/bin/7z"


def findLatestFile(wildcardPath):
    flist = glob.glob(wildcardPath)
    
    if len(flist) == 0:
            return None
    
    for i in range(len(flist)):
        statinfo = os.stat(flist[i])
        flist[i] = flist[i], statinfo.st_size, statinfo.st_ctime

    #too much work for simple thing, just find the max value, no need to actually sort
    flist.sort(key=operator.itemgetter(2), reverse=True)
    topitem = flist[0]
    return topitem[0]

def processBackupSection(config, section, datetimestr):
    backupDir = config.get(section, "backupDir")
    p7FullOptions = config.get(section, "p7FullOptions")
    p7DiffOptions = config.get(section, "p7DiffOptions")
    includeFileList = config.get(section, "includeFileList")
    excludeFileList = config.get(section, "excludeFileList")

    latest = findLatestFile(os.path.join(backupDir, fullBackupPrefix + "*"))

    print latest

    params = ""
    if latest is None:
        fullBackupPath = os.path.join(backupDir, fullBackupPrefix + datetimestr + ".7z")
        params = " a " + \
            p7FullOptions + " " + \
            fullBackupPath + " " + \
            "@" + includeFileList + " " + \
            "-xr@" + excludeFileList
        print "full"
    else:
        fullBackupPath = latest
        diffBackupPath = os.path.join(backupDir, diffBackupPrefix + datetimestr + ".7z")
        params = " u " + \
            p7DiffOptions + " " + \
            fullBackupPath +" " + \
            "-u- -up0q3x2z0!" + diffBackupPath +  " " +  \
            "@" + includeFileList + " " \
            "-xr@" + excludeFileList

#    e = "%s %s" (p7zCommand, params)
    print p7zCommand + params
    p = subprocess.Popen(p7zCommand + params, shell=True)
    retcode = os.waitpid(p.pid, 0)[1]

    return retcode


def backup(configfile, singleSection):
    config = ConfigParser.ConfigParser()
    
    if None == configfile:
        configfile = "backup.ini"
         
    config.read(configfile)
    
    #TODO: resolve how to deal with python mess regarding time with timezone info
    #datetimestr = datetime.utcnow().isoformat()
    datetimestr = strftime("%Y%m%dT%H%M%S")
    
    i = 0
    while(True):
        section = "backup" + str(i)
        if False == config.has_section(section):
            break
        
        if singleSection == None or singleSection == section : 
            print "Begin processing '" + section + "'" 
            retcode = processBackupSection(config, section, datetimestr)
            print "Done processing '" + section + "' with return code '" + str(retcode) + "'"
            
            if 0 != retcode:
                break
        
        i = i + 1

def usage():
    print "Baseline backup script"
    print "Options:"
    print "    c|config -- specify alternative config file"
    print "    s|section -- limit processing to specific section of the config file"

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvc:s:", 
            ["help", "version", "config=", "section="])
    except getopt.GetoptError, err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
        
    configfile = None
    section = None
    verbose = False
    
    for o, a in opts:
        if o in ("-v"):
            verbose = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("--version"):
            usage()
            sys.exit()
        elif o in ("-c", "--config"):
            configfile = a
        elif o in ("-s", "--section"):
            section = a
        else:
            assert False, "unhandled option"
    
    backup(configfile, section)

if __name__ == "__main__":
    main()
