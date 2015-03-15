#!/bin/bash

#
# This bash script will generate a tar.gz package of the last version of the
# git repository without the .git files and folders.
# The purpose of this action is to generate the package to publish.
#

archiveName=kdeServiceMenuOpenSubtitles_`date --rfc-3339=date`

git archive --format=tar.gz --prefix kdeServiceMenuOpenSubtitles/ -o $archiveName.tar.gz HEAD
