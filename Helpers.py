import os


def directoryHelper(retentionTime, backupDestination):
    # check if backupDestination exists
    if not os.path.isdir(backupDestination):
        os.system("mkdir " + backupDestination)
    else:
        # rotate backup directories
        directoryRotator(retentionTime, backupDestination)
    return 0


def directoryRotator(retentionTime, backupDestination):
    # remove oldest snapshot
    if os.path.isdir(backupDestination + 'backup.' + str(retentionTime)):
        os.system("rm -rf " + backupDestination + "backup." + str(retentionTime))

    # rotate backups one tier down
    for x in range(int(retentionTime) - 1, -1, -1):
        if os.path.isdir(backupDestination + 'backup.' + str(x)):
            os.system('mv ' + backupDestination + 'backup.' + str(x) + ' ' + backupDestination + 'backup.' + str(x+1))
    return 0


def createBackup0(backupDestination):
    # create backup.0 from .sync
    os.system("mv " + backupDestination + ".sync " + backupDestination + "backup.0")
    return 0


def configurationValidator(configuration):
    # check if configuration file exists
    if not os.path.isfile(configuration):
        print("No such configuration file!")
        exit(1)

    # check if backupDestination ends in /


    return 0
