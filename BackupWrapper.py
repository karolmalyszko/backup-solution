import os
import settings


class BackupWrapper:

    host = ''
    user = ''
    backupSource = ''
    backupDestination = ''
    command = ''
    arguments = ''

    def __init__(self, server):
        DEBUG = settings.debug

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

        if self.user and self.host:
            commandLine = "{} {} {}@{}:{} {}.sync".format(self.command, self.arguments, self.user, self.host,
                                                          self.backupSource, self.backupDestination)
            if DEBUG:
                print(commandLine)
        else:
            commandLine = "{} {} {} {}.sync".format(self.command, self.arguments, self.backupSource,
                                                    self.backupDestination)
            if DEBUG:
                print(commandLine)

        if DEBUG:
            print("Backup command to be executed :: " + commandLine)

        if DEBUG:
            returned_value = os.system(commandLine)
            print('Returned value :: ', returned_value)
        else:
            os.system(commandLine)
