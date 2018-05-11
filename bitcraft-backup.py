import sys
import getopt
import os
import json
from Helpers import directoryHelper
from Helpers import configurationValidator
from Helpers import executeSimpleBackupJob
from Helpers import executeRemoteScript
from Helpers import s3sync
import settings
import logging

DEBUG = settings.debug


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hc:", ["cfile="])
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                print('backup.py -c <configuration file>')
                sys.exit(0)
            elif opt in ("-c", "--cfile"):
                configfile = arg
                runBackup(configfile)
        if (len(args) == 0) and (len(opts) == 0):
            configfile = "configuration-main.json"
            runBackup(configfile)
    except getopt.GetoptError:
        print('backup.py -c <configuration file>')
        exit(1)


def runBackup(configfile):
    # verify if file exists
    if os.path.isfile(configfile):
        with open(configfile) as json_data:
            serverConfiguration = json.load(json_data)

            # iterate over elements in configuration file
            for server in serverConfiguration["server"]:
                server = configurationValidator(server)
                logging.basicConfig(level=logging.DEBUG,
                                    format='%(asctime)s %(levelname)-8s %(message)s',
                                    datefmt='%d-%m-%y %H:%M:%S',
                                    filename='/var/log/backup-solution/{}.log'.format(server["host"]),
                                    filemode='a'
                                    )
                logging.info("Running with configuration file :: {}".format(configfile))

                # assess directory structure
                directoryHelper(server["retentionPeriod"], server["backupDestination"])

                # assess if there is a script to execute on remote machine
                if "remoteScript" not in server:
                    executeSimpleBackupJob(server)
                else:
                    if server["remoteScript"] is not "":
                        # it appears that there in fact is a remote script
                        executeRemoteScript(server)
                        # and now backup the result of script execution
                        executeSimpleBackupJob(server)
                    else:
                        # no script but key exists in configuration file; run just the standard backup job
                        executeSimpleBackupJob(server)

                s3sync(server["backupDestination"], server["host"])

        logging.info("Finished job from configuration file.")
        exit(0)
    else:
        logging.error("Configuration file not found. Aborting execution.")
        exit(2)


# Script entrypoint
if __name__ == "__main__":
    main(sys.argv[1:])
