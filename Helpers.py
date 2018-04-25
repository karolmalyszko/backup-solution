import os


def directoryHelper(retentionTime, backupDestination):
    # check if backupDestination exists
    if not os.path.isdir( backupDestination ):
        os.system("mkdir " + backupDestination)
    else:
        # rotate backup directories
        directoryRotator(retentionTime, backupDestination)
    return 0


def directoryRotator(retentionTime, backupDestination):
    # remove oldest snapshot
    if os.path.isdir(backupDestination + '/backup.' + str(retentionTime)):
#        print("Removing directory backup." + str(retentionTime))
        os.system("rm -rf " + backupDestination + "/backup." + str(retentionTime))

    # rotate backups one tier down
    for x in range(int(retentionTime) - 1, -1, -1):
        if os.path.isdir(backupDestination + '/backup.' + str(x)):
#            print("Moving backup." + str(x) + " to backup." + str(x+1))
            os.system('mv ' + backupDestination + '/backup.' + str(x) + ' ' + backupDestination + '/backup.' + str(x+1))

    # create backup.0 from .sync
    os.system("mv " + backupDestination + "/.sync " + backupDestination + "/backup.0")

    return 0