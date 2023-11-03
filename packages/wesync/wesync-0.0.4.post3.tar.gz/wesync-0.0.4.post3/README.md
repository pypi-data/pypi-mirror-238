

# Usage

### General information

When you run the command in a directory that is known to the configuration (host and path both match), 
the default project and deployment are determined automatically and used in subsequent commands.

In that case there is no need to issue --project or --deployment commands

* `--workdir`: The working directory for wesync. Default is ~/wesync
* `--verbose`: Additional working information
* `--debug`: Also print debug messages
* `--stash`: The directory of the stash, relative to workdir. Default is stash 

## Snapshots

Snapshots are locally stored backups of the project according to it's configuration or type

It usually contains the database and one or more file archives.

### Create a new snapshot

```bash
wesync snapshot export --project <projectName> --deployment <deploymentName> [--only-database] [label]
```

This saves a snapshot locally.

* `label` Sets the label for the export. A random hex will be generated if missing

### Restore a snapshot

```bash
wesync snapshot import --project <projectName> --deployment <deploymentName> [--only-database] [--label <label>] [--path <path>]
```

This uses the local snapshot to restore the project database and files

* `--only-database`: This flag export/imports only the database from the snapshot
* `label`: Import the snapshot by the specified label
* `path`: Import the snapshot using the specified path.

If both path and label are missing, the most recent snapshot for the project will be imported.

### List snapshot

```bash
wesync snapshot list --project <projectName>
```

This list snapshots for the specified project. If project is omitted all snapshots are listed 

### Delete snapshots

```bash
wesync snapshot delete --project <projectName> --label <label> --path <path>
```

Delete a snapshot either by label or path. Project is required when deleting a single snapshot.

### Purge all snapshots


```bash
wesync snapshot purge --project <projectName>
```

Delete all snapshots for a project. If project name is omitted all snapshots will be deleted for all projects.

## Sync

The sync command uses different strategies to export data from a project and import it in another project in the same command
The command requires a project, a source and destination deployment

```bash
wesync sync --project <projectName> sourceDeployment destinationDeployment [--sync-strategy] [--only-database]
```

* `--only-database`: This flag syncs only the database between deployments
* `--sync-strategy`: Determines the method that sync will use. Options are described below

### Sync strategies
* `snapshot`: Export a snapshot on the sourceDeployment, copy it to the destinationDeployment using rsync, and import it
* `snapshotScp`: Same as snapshot, but transfer the data using scp instead of rsync
* `scp`: Stream the database and copy the files from source location to destination location using SCP
* `rsync`: Stream the database and sync the files from source location to destination location using rsync

Streaming the database implies piping the database export to the database import command


## Backups

The backup command uploads a project snapshot it to the backup location using SFTP.

```bash
wesync backup --project <projectName> push --backup my_location --label 37fca811 --replace --latest
```

* `--label <label>`: Label of the snapshot the will be pushed
* `--backup <name>`: Name of the configured backup location
* `--replace`: If the backup already exists on the backup location, replace it.
* `--latest`: Copy/restore the backup data to/from the latest folder. Overwrites the previous content

### Push & Pull
Use a label to identify the snapshot and then push it to backup or pull it from backup locally

### Export && Import
Export a snapshot and push it backup or fetch a snapshot from backup and import it

## Other commands

### Configuration update/push

* Create a new work directory

```bash
wesync config init
```

* Purge the work directory

```bash
wesync config purge [--full]
```

`--full`: Delete entire directory, not just configuration 

* update / commmit

```bash
wesync config update|commit
```

Fetches new configuration from the repository or commits changes and pushed to remote


# Building

Install build tools
```bash
pip3 install --upgrade build
pip3 install virtualenv
```

Go to project root directory and run build module

```bash
python3 -m build
```

Find the whl file and install it globally (for testing)
```bash
pip3 install --force-reinstall dist/wesync-0.0.1-py3-none-any.whl
```

Test the package:
```bash
wesync --help
python3
>>> import wesync

python3 -m wesync
```
