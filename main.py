import sys
import getopt
import os
import json
from BackupWrapper import BackupWrapper
from Helpers import directoryHelper
from Helpers import configurationValidator
from Helpers import createBackup0
import settings

DEBUG = settings.debug


def main(argv):
    configfile = ''
    try:
        opts, args = getopt.getopt(argv, "hc:", ["cfile="])
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                print('backup.py -c <configuration file>')
                sys.exit()
            elif opt in ("-c", "--cfile"):
                configfile = arg

                if DEBUG:
                    print("Reading from file :: " + str(configfile))

                runBackup(configfile)
            else:
                print("Opening ", configfile)
        if (len(args) == 0) and (len(opts) == 0):
            configfile = "configuration-main.json"

            if DEBUG:
                print("Reading from file :: " + str(configfile))

            runBackup(configfile)
    except getopt.GetoptError:
        print('backup.py -c <configuration file>')
        sys.exit(2)


def runBackup(configfile):
    # TODO logging to file
    # validate if file exists
    if os.path.isfile(configfile):
        with open(configfile) as json_data:
            serverConfiguration = json.load(json_data)

            # iterate over servers in configuration file
            for server in serverConfiguration["servers"]:
                server = configurationValidator(server)
                if "retentionPeriod" not in server:
                    print("Setting retention time to default.")
                    retentionTime = settings.defaultRetentionPeriod
                else:
                    retentionTime = server["retentionPeriod"]

                if DEBUG:
                    print("Retention time :: " + str(retentionTime))

                # assess directory structure
                directoryHelper(retentionTime, server["backupDestination"])

                # execute backup job to [backupDestination]/.sync
                # this is the equivalent of sync_first switch from rsnapshot
                backupCommand = str(BackupWrapper(server))
                if DEBUG:
                    print("Running backup job with :: " + backupCommand)
                os.system(backupCommand)
                '''try:
                    os.system(backupCommand)
                except:
                    print("Backup operation failed")
                    if DEBUG:
                        print(os.system(backupCommand))
                    exit(2)'''

                createBackup0(server["backupDestination"])

                syncCommand = "aws s3 sync {} s3://bitcraft.backup/{}".format(server["backupDestination"], server["host"])
                os.system(syncCommand)
        return 0
    else:
        print("You ungrateful bastard!")
        return 1


# Script entrypoint
if __name__ == "__main__":
    main(sys.argv[1:])
