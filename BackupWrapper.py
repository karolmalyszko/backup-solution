class BackupWrapper:

    host = ''
    user = ''
    backupSource = ''
    backupDestination = ''
    command = ''
    arguments = ''
    commandLine = ''
    remoteScript = ''

    def __init__(self, server, operationMode):
        if operationMode == 1:
            # basic backup
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
            else:
                self.commandLine = "{} {} {} {}.sync".format(self.command, self.arguments, self.backupSource,
                                                        self.backupDestination)
        elif operationMode == 2:
            # remote script execution
            self.host = (server["host"])
            self.user = (server["user"])
            self.remoteScript = (server["remoteScript"])
            self.commandLine = "ssh {}@{} {}".format(self.user, self.host, self.remoteScript)

    def __repr__(self):
        return str(self.commandLine)
