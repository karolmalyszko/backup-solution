import sys
import getopt
import os
import json
from BackupWrapper import BackupWrapper
from Helpers import directoryHelper
from Helpers import configurationValidator
from Helpers import createBackup0
import settings
import logging

DEBUG = settings.debug


def main(argv):
    # configfile = ''
    try:
        opts, args = getopt.getopt(argv, "hc:", ["cfile="])
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                print('backup.py -c <configuration file>')
                sys.exit(0)
            elif opt in ("-c", "--cfile"):
                configfile = arg
                # logging.info("Reading from file :: {}".format(configfile))
                runBackup(configfile)
#            else:
#                logging.info("Using configuration file :: ", configfile)
        if (len(args) == 0) and (len(opts) == 0):
            configfile = "configuration-main.json"
            # logging.info("Using default configuration file.")
            runBackup(configfile)
    except getopt.GetoptError:
        print('backup.py -c <configuration file>')
        exit(1)


def runBackup(configfile):
    # validate if file exists
    if os.path.isfile(configfile):
        with open(configfile) as json_data:
            serverConfiguration = json.load(json_data)

            # iterate over servers in configuration file
            for server in serverConfiguration["servers"]:
                server = configurationValidator(server)
                logging.basicConfig(level=logging.DEBUG,
                                    format='%(asctime)s %(levelname)-8s %(message)s',
                                    datefmt='%d-%m-%y %H:%M:%S',
                                    filename='/var/log/backup-solution/{}.log'.format(server["host"]),
                                    filemode='a'
                                    )
                if "retentionPeriod" not in server:
                    logging.info("Setting retention time to default.")
                    retentionTime = settings.defaultRetentionPeriod
                else:
                    retentionTime = server["retentionPeriod"]

                if DEBUG:
                    logging.debug("Retention time :: {}".format(retentionTime))

                # assess directory structure
                directoryHelper(retentionTime, server["backupDestination"])

                # execute backup job to [backupDestination]/.sync
                # this is the equivalent of sync_first switch from rsnapshot
                backupCommand = str(BackupWrapper(server))
                logging.info("Running backup job with :: " + backupCommand)
                os.system(backupCommand)

                createBackup0(server["backupDestination"])

                syncCommand = "aws s3 sync {} s3://bitcraft.backup/{}".format(server["backupDestination"], server["host"])
                os.system(syncCommand)
        exit(0)
    else:
        logging.error("Configuration file not found. Aborting execution.")
        exit(2)


# Script entrypoint
if __name__ == "__main__":
    main(sys.argv[1:])
