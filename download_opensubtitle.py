#!/usr/bin/python

# download_opensubtitle: KDE service menu for opensubtitles.org
# Copyright (C) 2007 Carlos Acedo
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

# Download subtitles from opensubtitles.org
# Default language is english, to change the language edit "subLanguage" in the
# "config" variable just after the includes.

# Original developer:
# Carlos Acedo (carlos@linux-labs.net)
# Inspired by subdownloader
# License GPL v2
#
# Maintainer from 2013-12-27:
# Nicola Felice (dev@dominiofelice.com)
# Original code was found in
# http://kde-look.org/content/show.php/download_opensubtitle?content=65444
#
# - The hash function have been copied from:
#   http://trac.opensubtitles.org/projects/opensubtitles/wiki/HashSourceCodes

import os, struct
from subprocess import check_output, call
from time import sleep
from sys import argv
import xmlrpclib
import socket

config = {
    'url': 'http://api.opensubtitles.org/xml-rpc',
    'userAgent': 'kdeServiceMenuOpensubtitles',
    'debug': True,
    'subLanguage': 'eng',
}

# if kdialog is not installed i must notify the user about the problem. I hope
# at least "konsole" is installed so i use "dialog" to display a message box
# for shell scripts.
# In Kubuntu 15.04 kdialog it's not installed by default but it's avaiable 
# inside the package "kde-baseapps-bin".
def fallbackKdialog():
    # use stdout anyway
    print "'kdialog' is required but failed to execute, check if it's installed"
    try:
        retCode = call(["konsole", "--version"])
        retCode = call(["dialog", "--version"])
        retCode = call('konsole -e dialog --msgbox "\'kdialog\' is required but failed to execute, check if it\'s installed" 8 76', shell=True);
    except(OSError):
        print "Even 'konsole' or 'dialog' are not available, message delivered only through stdout"
        
def checkRequirements():
    try:
        call(["kdialog", "--version"])
    except(OSError):
        fallbackKdialog()
        exit(1)    

    try:
        call(["wget", "--version"])
    except(OSError):
        showDialogError("'wget' is required but failed to execute, check if it's installed")
        exit(1)

    # no --version arg available for qdbus, no args will list available services
    try:
        call(["qdbus"])
    except(OSError):
        showDialogError("'qdbus' is required but failed to execute, check if it's installed")
        exit(1);

def hashFile(name):
    try:

        longlongformat = 'q'  # long long
        bytesize = struct.calcsize(longlongformat)

        f = open(name, "rb")

        filesize = os.path.getsize(name)
        hash = filesize

        if filesize < 65536 * 2:
            return "SizeError"

        for x in range(65536/bytesize):
            buffer = f.read(bytesize)
            (l_value,)= struct.unpack(longlongformat, buffer)
            hash += l_value
            hash = hash & 0xFFFFFFFFFFFFFFFF #to remain as 64bit number


        f.seek(max(0,filesize-65536),0)
        for x in range(65536/bytesize):
            buffer = f.read(bytesize)
            (l_value,)= struct.unpack(longlongformat, buffer)
            hash += l_value
            hash = hash & 0xFFFFFFFFFFFFFFFF

        f.close()
        returnedhash =  "%016x" % hash
        return returnedhash

    except(IOError):
        return "IOError"

def showDialogError(message):
    os.system('kdialog --title "OpenSubtitles.org downloader" --error "' + message + '"')

def showDialogSelect(items):
    command = 'kdialog'
    command += ' --geometry 400x200'
    command += ' --title "OpenSubtitles.org downloader"'
    command += ' --menu "Select subtitle"'
    command += ' ' + items
    return os.popen(command).readline()

def showProgressBar():
    return check_output(['kdialog',
                        '--title', 'OpenSubtitles.org downloader',
                        '--progressbar', 'Downloading subtitle...', '3'])

def showDialogOverwrite(fileName):
    return call(['kdialog',
                 '--title', 'OpenSubtitles.org downloader',
                 '--warningyesno', 'A file named "' + fileName + '" already exists.\nDo you want to replace it with the new downloaded subtitle?'])

# ================== Main program ========================

checkRequirements()
server = xmlrpclib.ServerProxy(config['url'], verbose=config['debug'])
peli = argv[1]

try:
    myhash = hashFile(peli)
    size = os.path.getsize(peli)
    session =  server.LogIn("","", config['subLanguage'], config['userAgent'])

    if session["status"] != "200 OK":
        showDialogError('"Login failed:\n' + session["status"] + '"')
        exit(1)

    token = session["token"]

    searchlist = []
    searchlist.append({
        'sublanguageid': config['subLanguage'],
        'moviehash': myhash,
        'moviebytesize': str(size)
        })

    moviesList = server.SearchSubtitles(token, searchlist)
    if moviesList['data']:
        mindex = 0
        kdialog_items = ''
        for item in moviesList['data']:
            kdialog_items = kdialog_items + '"' + str(mindex) + '" "' + item['SubFileName'] + '" '
            mindex = mindex + 1

        resp = showDialogSelect(kdialog_items)
        # check if the user pressed "cancel".
        # If the user has no selected a subtitle and pressed "ok" the first
        # subtitle will be chosen
        if resp == '':
            exit(0)

        subFileName = os.path.basename(peli)[:-3] + moviesList['data'][int(resp)]['SubFileName'][-3:]
        subDirName = os.path.dirname(peli)
        subURL = moviesList['data'][int(resp)]['SubDownloadLink']

        # Ask before overwriting an existing subtitle
        if os.path.isfile(subDirName + '/' + subFileName):
            resp = showDialogOverwrite(subFileName)
            print resp
            if resp == 1:
                exit(0)

        #return value have a trailing newline so it must be stripped
        dbusRef = showProgressBar().strip()

        #Update progressbar to 30%
        os.system('qdbus '+ str(dbusRef).strip() + ' Set "" value 1')
        response = os.system('wget -O - ' + subURL + ' | gunzip  > "' + subDirName + '/' + subFileName + '"' )
        print 'wget -O - ' + subURL + ' | gunzip  > "' + subDirName + '/' + subFileName + '"'

        #Display 100% for a second, then close
        os.system('qdbus '+ str(dbusRef) + ' Set "" value 3')
        os.system('qdbus '+ str(dbusRef) + ' setLabelText "Subtitle downloaded and unpacked"')
        sleep(1)
        os.system('qdbus '+ str(dbusRef) + ' close')

        if response != 0:
            showDialogError('An error ocurred downloading or writing the subtitle')

    else:
        showDialogError('No subtitles found\n\nYou can try searching manually on opensubtitles.org')

    server.Logout(session["token"])
except xmlrpclib.Error, err:
    #for testing this error, change the url with a non xmlrpc server
    message = 'An error ocurred contacting the OpenSubtitles.org server:\n\n'
    message += 'Error ' + str(err.errcode) +  ': ' + err.errmsg
    showDialogError(message);
except socket.error, err:
    #for testing this error, disable the internet connection
    showDialogError('Unable to contact the OpenSubtitles.org server:\n\n' + err[1])
