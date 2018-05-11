import os
import settings
import datetime
import logging
from BackupWrapper import BackupWrapper

DEBUG = settings.debug


def directoryHelper(retentionTime, backupDestination):
    # check if backupDestination exists
    if not os.path.isdir(backupDestination):
        logging.info("Creating '{}' directory".format(backupDestination))
        os.system("mkdir -p {}".format(backupDestination))
    else:
        # rotate backup archives
        fileRotator(retentionTime, backupDestination)
    return 0


def fileRotator(retentionTime, backupDestination):
    # remove oldest snapshot
    if os.path.isfile("{}backup.{}.tar.gz".format(backupDestination, retentionTime)):
        logging.info("Removing oldest backup dir")
        os.system("rm -f {}backup.{}.tar.gz".format(backupDestination, retentionTime))

    # rotate backups one tier down
    logging.info("Rotating backups")
    for x in range(int(retentionTime) - 1, -1, -1):
        if os.path.isfile("{}backup.{}.tar.gz".format(backupDestination, x)):
            os.system("mv {}backup.{}.tar.gz {}backup.{}.tar.gz".format(backupDestination, x, backupDestination, x+1))
            logging.info("moving archives {}backup.{} to {}backup.{}".format(backupDestination, x, backupDestination, x+1))
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
    # syncCommand = "aws s3 sync {} s3://bitcraft.backup/{} --only-show-errors".format(backupDestination, host)
    syncCommand = "aws s3 cp {}*.tar.gz s3://bitcraft.backup/{}/ --only-show-errors".format(backupDestination, host)
    if DEBUG:
        logging.debug(syncCommand)
    logging.info("Syncing {} with directory {} on S3".format(backupDestination, host))
    os.system(syncCommand)
    return 0


def executeSimpleBackupJob(server):
    # execute backup job to [backupDestination]/.sync
    # this is the equivalent of sync_first switch from rsnapshot
    backupCommand = str(BackupWrapper(server, 1))
    logging.info("Running backup job with :: " + backupCommand)
    os.system(backupCommand)

    createBackup0(server["backupDestination"])

    compressBackup(server["backupDestination"])
    return 0


def executeRemoteScript(server):
    backupCommand = str(BackupWrapper(server, 2))
    logging.info("Running script on remote machine with :: " + backupCommand)
    os.system(backupCommand)
    return 0


def compressBackup(destination):
    if DEBUG:
        parameters = 'czvf'
    else:
        parameters = 'czf'

    compressCommand = "tar -{} {}backup.0.tar.gz {}backup.0".format(parameters, destination, destination)

    if DEBUG:
        logging.debug("Compressing backup with command :: " + compressCommand)
    else:
        logging.info("Compressing backup.")

    os.system(compressCommand)

    logging.info("Removing directory backup.0")
    os.system("rm -rf {}backup.0".format(destination))

    return 0
