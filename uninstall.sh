#!/bin/bash

fileDesktop=download_opensubtitle.desktop
fileScript=download_opensubtitle.py
folderDesktop=~/.kde/share/kde4/services/ServiceMenu
folderScript=/usr/local/bin

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