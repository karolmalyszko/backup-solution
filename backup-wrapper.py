import os


host = "bitcraft-dns"
user = "sonny"
backupSource = "/etc/bind/"
backupDestination = "./bitcraft-testing"
command = "rsync"
arguments = "-ravzX --delete"

commandLine = command + " " + arguments + " " + user + "@" + host + ":" + backupSource + " " + backupDestination

returned_value = os.system(commandLine)
print('Returned value :: ', returned_value)
