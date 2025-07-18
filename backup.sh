#!/bin/bash

# Set variables
BACKUP_DIR="/backup"
DATE=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/notesdb_$DATE.sql"

# Create backup
mysqldump -u notesuser -ppassword123 notesdb > $BACKUP_FILE

# Compress backup
gzip $BACKUP_FILE

echo "Backup completed: ${BACKUP_FILE}.gz"

