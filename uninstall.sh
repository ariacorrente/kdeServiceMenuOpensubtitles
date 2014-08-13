#!/bin/bash

fileDesktop=download_opensubtitle.desktop
fileScript=download_opensubtitle.py
folderDesktop=`kde4-config --path services | cut -d : -f 1`
folderScript=`echo $PATH | cut -d : -f 1`
folderScript=`kde4-config --install exe | cut -d : -f 1`

echo
echo download_opensubtitle service menu uninstaller
echo The script will ask your confirmation before removing every file.
echo

# Service menu
rm -i $folderDesktop/$fileDesktop

# Installs the python script in a folder in the PATH
echo
echo I may need the sudo password to remove the python script from \"$folderScript\"
sudo rm -i $folderScript/$fileScript
