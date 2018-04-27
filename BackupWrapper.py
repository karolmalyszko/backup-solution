#import settings


class BackupWrapper:

    host = ''
    user = ''
    backupSource = ''
    backupDestination = ''
    command = ''
    arguments = ''
    commandLine = ''

    def __init__(self, server):
#        DEBUG = settings.debug
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
            self.commandLine = "{} {} {}@{}:{} {}.sync".format(self.command, self.arguments, self.user, self.host,
                                                          self.backupSource, self.backupDestination)
#            if DEBUG:
#                print(self.commandLine)
        else:
            self.commandLine = "{} {} {} {}.sync".format(self.command, self.arguments, self.backupSource,
                                                    self.backupDestination)
#            if DEBUG:
#                print(self.commandLine)

#        if DEBUG:
#            print("Backup command to be executed :: " + self.commandLine)

        # return self.commandLine

    def __repr__(self):
        return str(self.commandLine)
