#!/bin/bash 
DATE=$(date +%Y%m%d) 
BACKUP_DIR="Insert file location here/$DATE" 
SOURCE_DIR=$MYSCRATCH
mkdir -p $BACKUP_DIR 
tar -czf "$BACKUP_DIR/files.tar.gz" $SOURCE_DIR 
