#!/usr/bin/python -o

import utils

def buildLocalDirString(localDirs, sep):
    empty = True
    for local in localDirs:
        if (empty):
            localDirString = local
        else:
            localDirString += sep + local
    return localDirString

def writeSlavesFile(slaves):
    f = open('slaves', 'w')
    for slave in slaves:
        f.write(slave + "\n")
    f.close()

def setupConf(master, slaves, port, javahome, localDirString):
    # copy templates to conf
    utils.cmd("rm -rf conf; cp -r hadoop1-template conf")
    
    # setup conf with the details
    utils.cmd("cd conf; sh mr1-setup-conf.sh " + master + " " + port + " " + javahome + " " + localDirString + "; cd ..")
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

def deploy(user, master, fileName, dirName, destLoc, localDirs):
    localDirString = buildLocalDirString(localDirs, ' ')
    cmd = "mkdir -p " + destLoc + ";"
    cmd += "rm -rf " + localDirString + ";"
    cmd += "rm -rf " + destLoc + "/" + dirName + "*;"
    cmd += "mkdir -p " + localDirString + ";"
    utils.cmd_on_remote(master, user, cmd)
    utils.copy_to_remote(master, user, fileName, destLoc)
    utils.cmd_on_remote(master, user, "cd " + destLoc + ";tar -xzf " + fileName + ";chmod +x " + dirName + "/sbin/*")    

def install(options):
    [fileName, dirName] = getFileAndDirNames(options.tarball)
    if ("clean" in options.args):
        setupConf(options.master, options.machines, options.port, options.javahome, buildLocalDirString(options.localDirs, ','))
        buildTarBall(options.tarball, fileName, dirName)
        
    deploy(options.user, options.master, fileName, dirName, options.destLoc, options.localDirs)
    for slave in options.machines:
        deploy(options.user, slave, fileName, dirName, options.destLoc, options.localDirs)

def main():
    options = utils.MyOptions()
    if options.parse_args():
        install(options)

if __name__ == "__main__":
    main()
