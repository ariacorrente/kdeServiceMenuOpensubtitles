#!/bin/bash

# Paths
fileDesktop=download_opensubtitle.desktop
fileScript=download_opensubtitle.py
folderDesktop=`kde4-config --path services | cut -d : -f 1`
folderScript=`kde4-config --install exe | cut -d : -f 1`

echo
echo download_opensubtitle service menu installer
echo The following files will be installed:
echo - \"$fileDesktop\" into \"$folderDesktop\"
echo - \"$fileScript\" into \"$folderScript\"
echo

# Service menu
mkdir -p $folderDesktop
cp -i $fileDesktop $folderDesktop

# Installs the python script in a folder in the PATH
echo
echo I may need the sudo password to copy the python script to \"$folderScript\"
sudo cp -i $fileScript $folderScript
