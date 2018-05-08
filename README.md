Backup solution designed specifically for pulling backups from **remote** machines and then syncing them to protected Amazon S3 bucket.

**Usage**

`python bitcraft-backup.py -c /absolute/path/to/configuration/file.json`

**Configuration file syntax**

You can put multiple server blocks inside one configuration file.

```json
{
  "servers" : [
    {
      "host" : "localhost",
      "user" : "sonny",
      "backupSource" : "/home/",
      "backupDestination" : "localhost/",
      "command" : "rsync",
      "arguments" : "-ravzX --delete"
    },
    {
      "host" : "bitcraft-dns",
      "user" : "sonny",
      "backupSource" : "/etc/bind/",
      "backupDestination" : "bitcraft-dns/",
      "command" : "rsync",
      "arguments" : "-ravzX --delete",
      "remoteScript" : ""
    }
  ]
}
```

Default configuration switches are included in settings-base.py file. Before first run, rename this file to settings.py and change contents if required.

Also before first run, create directory _/var/log/backup-solution_ and change it's owner to user running the backup script

**Absolutely required fields ::**

- **backupSource** - path to directory/file on remote machine

- **user** for passwordless connecting to remote machine

- **host** to back up

For server and user configuration instructions and prerequisites, go to ::
https://confluence.bitcraft.com.pl/display/TEC/Virtual+Machines%2C+applications+and+configurations+backup+policy+and+setup
