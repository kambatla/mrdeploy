#!/usr/bin/python -o

import getpass
from optparse import OptionParser
import os

PREAMBLE = ' ------------------------- '
SSH = 'ssh -o StrictHostKeyChecking=no '
SCP = 'scp -r -o StrictHostKeyChecking=no '

def output(cmd):
    out = os.system(cmd)
    if out == 0:
        return " ... OK"
    else:
        return " ... FAIL"

# Execute command locally
def cmd(cmd):
    print cmd + output(cmd)

# From user@host string
def remote(user, host):
    return user + '@' + host

# execute command on a remote machine
def cmd_on_remote(host, user, cmd):
    command = SSH + remote(user, host) + ' "' + cmd + '"'
    print host + ' ' + output(command)

# execute command on a list of machines
def cmd_on_remoteList(hostList, user, cmd):
    for host in hostList:
	print PREAMBLE + host + PREAMBLE
        cmd_on_remote(host, user, cmd)

# copy files to a remote machine
def copy_to_remote(host, user, fromPath, toPath):
    command = SCP + fromPath + ' ' + remote(user,host) + ':' + toPath
    print host + ' ' + output(command)
    
# copy files from a remote machine
def copy_from_remote(host, user, fromPath, toPath):
    command = SCP + user + '@' + host + ':' + fromPath + ' ' + toPath
    print host + ' ' + output(command)

# copy to a list of machines
def copy_to_remoteList(hostList, user, fromPath, toPath):
    for host in hostList:
        copy_to_remote(host, user, fromPath, toPath)

# build a list from given prefix and range
def machineList_from_range(hostPrefix, rangeLow, rangeHigh):
    machineList = []
    for i in range(rangeLow, rangeHigh + 1):
        machineList.append(hostPrefix + `i`)
    return machineList

def printUsage():
    print("Require argumets: -s <slaves> -m <master> -p <port> -b <hadoop tarball>")

class MyOptions:
    '''
    Returns true for succesful parse and false otherwise
    '''
    def parse_args(self):
        parser = OptionParser()
        parser.add_option("-s", "--slaves", dest="target",
                          help="slave nodes (or prefix if using range)")
        parser.add_option("-r", "--range", dest="targetRange",
                          help="range of machines")
        parser.add_option("-m", "--master", dest="master",
                          help="hadoop cluster master")
        parser.add_option("-p", "--port", dest="port",
                          help="base port for hadoop")
        parser.add_option("-b", "--ball", dest="tarball",
                          help="hadoop tar ball")
        parser.add_option("-d", "--destLoc", dest="destLoc",
                          help="hadoop location on destinaton nodes")
        parser.add_option("-j", "--javahome", dest="javahome",
                          help="JAVA_HOME for hadoop-env")

        (options, args) = parser.parse_args()

        if any([not options.master,
                not options.port,
                not options.target,
                not options.tarball,
                not options.destLoc,
                not options.javahome]):
            parser.print_help()
            return False

        targetList = [dest.strip() for dest in options.target.split(',')]
        if not (options.targetRange):
            destList = targetList
        else:
            rangeList = [rng.strip() for rng in options.targetRange.split(',')]
            destList = machineList_from_range(targetList[0], int(rangeList[0]), int(rangeList[1]))

        self.machines = destList
        self.master = options.master
        self.port = options.port
        self.tarball = options.tarball
        self.user = getpass.getuser()
        self.destLoc = options.destLoc
        self.javahome = options.javahome
        self.args = args
        return True
