#!/bin/bash

#
# This bash script will generate a tar.gz package of the last version of the
# git repository without the .git files and folders.
# The purpose of this action is to generate the package to publish.
#
# WARNING!
# In kde-apps.org I can't upload a file because the website throws an error. I 
# solved the problem tagging a release in GitHub and linking to the archive
# generated automatically.
#

archiveName=kdeServiceMenuOpenSubtitles_`date --rfc-3339=date`

git archive --format=tar.gz --prefix kdeServiceMenuOpenSubtitles/ -o release/$archiveName.tar.gz HEAD
