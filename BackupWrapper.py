import os


class BackupWrapper:

    host = ''
    user = ''
    backupSource = ''
    backupDestination = ''
    command = ''
    arguments = ''

    def __init__(self, server):
        self.host = (server["host"])
        self.user = (server["user"])
        self.backupSource = (server["backupSource"])
        self.backupDestination = (server["backupDestination"])
        self.command = (server["command"])
        self.arguments = (server["arguments"])

        commandLine = self.command + " " + self.arguments + " " + self.user + "@" + self.host + ":" + self.backupSource + " " + self.backupDestination + ".sync"

        returned_value = os.system(commandLine)
        print('Returned value :: ', returned_value)
