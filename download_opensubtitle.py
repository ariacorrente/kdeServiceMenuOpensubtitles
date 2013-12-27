#!/usr/bin/python

# Download subtitles from opensubtitles.org
# Default language is english, to change the language change sublanguageid parameter
# in the searchlist.append function

# Carlos Acedo (carlos@linux-labs.net)
# Inspired by subdownloader
# License GPL v2

# Nicola Felice (dev@dominiofelice.com)
# 2013-12-27 Updating the script to let it work with changes the API
#
# - The hash function have been copied from:
#   http://trac.opensubtitles.org/projects/opensubtitles/wiki/HashSourceCodes

import os, struct
from subprocess import check_output
from time import sleep
from sys import argv
from xmlrpclib import ServerProxy, Error

config = {
    'url': 'http://api.opensubtitles.org/xml-rpc',
    'userAgent': 'OS Test User Agent', #only for test purposes
    'debug': True,
    'subLanguage': 'eng',
}

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
    os.system('kdialog --title "OpenSubtitles.org downloader" --error ' + message)

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

# ================== Main program ========================

server = ServerProxy(config['url'], verbose=config['debug'])
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
        #return value have a trailing newline so it must be stripped
        dbusRef = showProgressBar().strip()
        subFileName = os.path.basename(peli)[:-3] + moviesList['data'][int(resp)]['SubFileName'][-3:]
        subDirName = os.path.dirname(peli)
        subURL = moviesList['data'][int(resp)]['SubDownloadLink']
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
        showDialogError('No subtitles found')

    server.Logout(session["token"])
except Error, v:
    showDialogError('An error ocurred')



