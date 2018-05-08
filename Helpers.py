import os
import settings
import datetime
import logging

DEBUG = settings.debug


def directoryHelper(retentionTime, backupDestination):
    # check if backupDestination exists
    if not os.path.isdir(backupDestination):
        logging.info("Creating 'backupDestination' directory")
        os.system("mkdir -p {}".format(backupDestination))
    else:
        # rotate backup directories
        directoryRotator(retentionTime, backupDestination)
    return 0


def directoryRotator(retentionTime, backupDestination):
    # remove oldest snapshot
    if os.path.isdir("{}backup.{}".format(backupDestination, retentionTime)):
        logging.info("Removing oldest backup dir")
        os.system("rm -rf {}backup.{}".format(backupDestination, retentionTime))

    # rotate backups one tier down
    logging.info("Rotating backups")
    for x in range(int(retentionTime) - 1, -1, -1):
        if os.path.isdir("{}backup.{}".format(backupDestination, x)):
            os.system("mv {}backup.{} {}backup.{}".format(backupDestination, x, backupDestination, x+1))
            logging.info("moving {}backup.{} to {}backup.{}".format(backupDestination, x, backupDestination, x+1))
    return 0


def createBackup0(backupDestination):
    # create backup.0 from .sync
    os.system("cp -al {}.sync {}backup.0".format(backupDestination, backupDestination))
    logging.info("copying {}.sync to {}backup.0".format(backupDestination, backupDestination))
    # additional backup creation time info; has to have non-0 length for proper S3 sync
    os.system("echo {} > {}backup.0/{}.timestamp".format(datetime.datetime.now().strftime("%d-%m-%Y"),
                                                         backupDestination,
                                                         datetime.datetime.now().strftime("%d-%m-%Y")))
    return 0


def configurationValidator(configuration):
    # check if backupDestination key exists
    if "backupDestination" not in configuration:
        logging.warning("No backupDestination key present. Setting to default.")
        configuration["backupDestination"] = settings.defaultBackupDestination

    # check if backupDestination ends in /
    if not str(configuration["backupDestination"]).endswith("/"):
        logging.error("Incorrect 'backupDestination' path, must end with /")
        exit(3)

    # check if user key exists; not sure if it is really necessary, may be included in backupSource key
    if "user" in configuration:
        # check if host key exists
        if "host" in configuration:
            # check if user exists when host is not localhost
            if str(configuration["host"]) is not "localhost":
                if str(configuration["user"]) is "":
                    logging.error("No user present. This ain't gonna work. Fix it!")
                    exit(4)
        else:
            logging.error("No host present, but user is. This does not look right. Think it trough. Terminating.")
            exit(5)

    # check if backupSource key exists
    if "backupSource" not in configuration:
        logging.error("Nothng to backup. Really?")
        exit(6)

    # check if command key exists
    if "command" not in configuration:
        logging.warning("Setting command to defaults.")
        configuration["command"] = settings.defaultCommand

    # check if arguments key exists
    if "arguments" not in configuration:
        logging.warning("Setting arguments to defaults.")
        configuration["arguments"] = settings.defaultArguments

    if "retentionPeriod" not in configuration:
        logging.warning("Retention period not present in configuration file. Setting to default value.")
        configuration["retentionPeriod"] = settings.defaultRetentionPeriod

    return configuration


def s3sync(backupDestination, host):
    syncCommand = "aws s3 sync {} s3://bitcraft.backup/{}".format(backupDestination, host)
    logging.info("Syncing {} with directory {} on S3".format(backupDestination, host))
    os.system(syncCommand)
    return 0
