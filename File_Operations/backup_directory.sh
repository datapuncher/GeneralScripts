#!/usr/bin/bash

SOURCE="/path/to/working"
BACKUP="/path/to/backup"

# Delete the 'backup' directory for testing
# whether the script errors out or not.
# Change the path to 'backup'
trap 'rm -rf /home/jporta/backup' EXIT

echo "Backing up directory $SOURCE to $BACKUP"

rsync -a --delete "$SOURCE" "$BACKUP"

# Error handling when SOURCE directory is missing 
if [ $? -ne 0 ]; then
	exit 1
fi

echo "Backup successfully completed"
