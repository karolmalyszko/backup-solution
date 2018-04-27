import os
import settings
import datetime

DEBUG = settings.debug

def directoryHelper(retentionTime, backupDestination):
    # check if backupDestination exists
    if not os.path.isdir(backupDestination):
        if DEBUG:
            print("Creating 'backupDestination' directory")
        os.system("mkdir " + backupDestination)
    else:
        # rotate backup directories
        if DEBUG:
            print("Rotating directories")
        directoryRotator(retentionTime, backupDestination)
    return 0


def directoryRotator(retentionTime, backupDestination):
    # remove oldest snapshot
    if os.path.isdir(backupDestination + 'backup.' + str(retentionTime)):
        if DEBUG:
            print("Removing oldest backup dir")
        os.system("rm -rf " + backupDestination + "backup." + str(retentionTime))

    # rotate backups one tier down
    if DEBUG:
        print("Rotating backups")
    for x in range(int(retentionTime) - 1, -1, -1):
        if os.path.isdir(backupDestination + 'backup.' + str(x)):
            os.system('mv ' + backupDestination + 'backup.' + str(x) + ' ' + backupDestination + 'backup.' + str(x+1))
    return 0


def createBackup0(backupDestination):
    # create backup.0 from .sync
    if DEBUG:
        print("Creating backup.0")
    os.system("cp -al " + backupDestination + ".sync " + backupDestination + "backup.0")
    os.system("touch {}backup.0/{}".format(backupDestination, datetime.datetime.now().strftime("%d-%m-%Y")))
    return 0


def configurationValidator(configuration):
    # check if backupDestination key exists
    if "backupDestination" not in configuration:
        print("No backupDestination key present. Setting to default.")
        configuration["backupDestination"] = settings.defaultBackupDestination

    # check if backupDestination ends in /
    if not str(configuration["backupDestination"]).endswith("/"):
        print("Incorrect 'backupDestination' path, must end with /")
        exit(1)

    # check if user key exists; not sure if it is really necessary, may be included in backupSource key
    if "user" in configuration:
        # check if host key exists
        if "host" in configuration:
            # check if user exists when host is not localhost
            if str(configuration["host"]) is not "localhost":
                if str(configuration["user"]) is "":
                    print("No user present. This ain't gonna work. Fix it!")
                    exit(1)
        else:
            print("No host present, but user is. This does not look right. Think it trough. Terminating.")
            exit(1)

    # check if backupSource key exists
    if "backupSource" not in configuration:
        print("Nothng to backup. Really?")
        exit(1)

    # check if command key exists
    if "command" not in configuration:
        print("Setting command to defaults.")
        configuration["command"] = settings.defaultCommand

    # check if arguments key exists
    if "arguments" not in configuration:
        print("Setting arguments to defaults.")
        configuration["arguments"] = settings.defaultArguments

    return configuration
