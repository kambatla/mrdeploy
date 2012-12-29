#!/usr/bin/python -o

import utils

def writeSlavesFile(slaves):
    f = open('slaves', 'w')
    for slave in slaves:
        f.write(slave + "\n")
    f.close()

def setupConf(master, slaves, port, javahome):
    # copy templates to conf
    utils.cmd("rm -rf conf; cp -r hadoop1-template conf")
    
    # setup conf with the details
    utils.cmd("cd conf; sh mr1-setup-conf.sh " + master + " " + port + " " + javahome + "; cd ..")
    writeSlavesFile(slaves)
    utils.cmd("cp slaves conf/slaves")

def buildTarBall(tarball, fileName, dirName):
    confdir = dirName + "/etc/hadoop/"
    utils.cmd("rm -rf " + dirName)
    utils.cmd("tar -xzf " + tarball)
    utils.cmd("cp conf/* " + confdir)
    utils.cmd("tar -czf " + fileName + " " + dirName)
    utils.cmd("rm -rf conf slaves " + dirName)   

def getFileAndDirNames(tarball):
    fileName = tarball.rpartition('/')[2]
    if "SNAPSHOT" in fileName:
        dirParts = fileName.partition('SNAPSHOT')
        dirName = dirParts[0] + dirParts[1]
    else:
        dirName = fileName.partition('.tar.gz')[0]

    return [fileName, dirName];

'''
Deploy to an NFS based cluster - enough to copy to one node
'''
def deployNFS(user, master, fileName, dirName, destLoc):
    utils.cmd_on_remote(master, user, "mkdir -p " + destLoc + "; rm -rf " + destLoc + "/" + dirName + "*")
    utils.copy_to_remote(master, user, fileName, destLoc)
    utils.cmd_on_remote(master, user, "cd " + destLoc + ";tar -xzf " + fileName + ";chmod +x " + dirName + "/sbin/*")    

def install(options):
    [fileName, dirName] = getFileAndDirNames(options.tarball)
    if ("clean" in options.args):
        setupConf(options.master, options.machines, options.port, options.javahome)
        buildTarBall(options.tarball, fileName, dirName)
        
    deployNFS(options.user, options.master, fileName, dirName, options.destLoc)
    for slave in options.machines:
        deployNFS(options.user, slave, fileName, dirName, options.destLoc)

def main():
    options = utils.MyOptions()
    if options.parse_args():
        install(options)

if __name__ == "__main__":
    main()
