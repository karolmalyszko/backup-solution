Backup solution designed specifically for pulling backups from **remote** machines and then syncing them to protected Amazon S3 bucket.

**Usage**

`python bitcraft-backup.py -c /absolute/path/to/configuration/file.json`

**Configuration file syntax**

You can put multiple server blocks inside one configuration file.

```json
{
  "servers" : [
    {
      "host" : "<name or IP address of remote host>",
      "user" : "<user able to connect to remote host without password>",
      "backupSource" : "<file or directory to backup>",
      "backupDestination" : "<directory for storing backed-up files, must end with '/'; defaults to '/tmp' if not provided>",
      "command" : "<command to create backup with, defaults to 'rsync' if not provided>",
      "arguments" : "<additional arguments for command, defaults to '-ravzX --delete' if not provided>",
      "remoteScript" : "<absolute path to script performing additional operations; optional>",
      "retentionPeriod" : "<determines how many backups to retain; defaults to 7 if not provided>"
    },
    {
      "host" : "<name or IP address of remote host>",
      "user" : "<user able to connect to remote host without password>",
      "backupSource" : "<file or directory to backup>",
      "backupDestination" : "<directory for storing backed-up files, must end with '/'; defaults to '/tmp' if not provided>",
      "command" : "<command to create backup with, defaults to 'rsync' if not provided>",
      "arguments" : "<additional arguments for command, defaults to '-ravzX --delete' if not provided>",
      "remoteScript" : "<absolute path to script performing additional operations; optional>",
      "retentionPeriod" : "<determines how many backups to retain; defaults to 7 if not provided>"
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
