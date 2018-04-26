import os


class BackupWrapper:

    host = ''
    user = ''
    backupSource = ''
    backupDestination = ''
    command = ''
    arguments = ''

    def __init__(self, server):
        if "host" in server:
            self.host = (server["host"])
        else:
            self.host = None
        if "user" in server:
            self.user = (server["user"])
        else:
            self.user = None

        self.backupSource = (server["backupSource"])
        self.backupDestination = (server["backupDestination"])
        self.command = (server["command"])
        self.arguments = (server["arguments"])

        commandLine = self.command + " " + self.arguments

        if self.user and self.host:
            commandLine = commandLine + " " + self.user + "@" + self.host + ":"
        else:
            commandLine = commandLine + self.backupSource + " " + self.backupDestination + ".sync"

        # os.system(commandLine)
        returned_value = os.system(commandLine)
        print('Returned value :: ', returned_value)
