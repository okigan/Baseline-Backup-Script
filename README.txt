#backup.ini -- configuration file for the Baseline Backup Script

#line strating with # are ignored

# Baseline Backup Script -- the baseline in automated backup
#  * Creates FULL backup of specified files, followed by
#  * Differencial backup which record new/changed and deleted files.
#
# Restore is done through 7z extraction of corresponding FULL backup 
# archive and (optionally) followed by extraction of corresponding Differenctial
# backup archive.

# The configuration file consists of sections. Sections named "backup<#>"
# are processed by the backup script which looks for following control keys:
#  * backupDir -- location where backup files will be created
#  * p7FullOptions -- 7z (compresson) options to be used during full backup
#  * p7DiffOptions -- 7z (compresson) options to be used during differencial backup
#      NOTE: incremental backup not supported (yet!?)
#  * includeFileList -- path to include file list (see 7z documentation)
#  * excludeFileList -- path to exclude file list (see 7z documentation)
