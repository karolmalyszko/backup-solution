import sys
import getopt
import os
import json
from BackupWrapper import BackupWrapper
from Helpers import directoryHelper
from Helpers import configurationValidator
from Helpers import createBackup0

# global variables
defaultBackupRetentionPeriod = 7


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
                runBackup(configfile)
            else:
                print("Opening ", configfile)
        if (len(args) == 0) and (len(opts) == 0):
            configfile = "configuration-main.json"
            runBackup(configfile)
    except getopt.GetoptError:
        print('backup.py -c <configuration file>')
        sys.exit(2)


def runBackup(configfile):
    # validate if file exists
    if os.path.isfile(configfile):
        with open(configfile) as json_data:
            serverConfiguration = json.load(json_data)

            # iterate over servers in configuration file
            for server in serverConfiguration["servers"]:
                server = configurationValidator(server)
#                if "retentionPeriod" not in server:
#                    retentionTime = defaultBackupRetentionPeriod
#                else:
#                    retentionTime = server["retentionPeriod"]

                # asses directory structure
                directoryHelper(retentionTime, server["backupDestination"])

                # execute backup job to [backupDestination]/.sync
                BackupWrapper(server)
                createBackup0(server["backupDestination"])

        # sync backup directories with S3 bucket
        return 0
    # validate JSON contents
    else:
        print("You ungrateful bastard!")
        return 1


# Script entrypoint
if __name__ == "__main__":
    main(sys.argv[1:])
