#!/usr/bin/python

# Download subtitles from opensubtitles.org
# Default language is english, to change the language change sublanguageid parameter
# in the searchlist.append function

# Carlos Acedo (carlos@linux-labs.net)
# Inspired by subdownloader
# License GPL v2

import os
from struct import *
from sys import argv
from xmlrpclib import ServerProxy, Error

def hashFile(name): 
      try: 
                 
                longlongformat = 'LL'  # signed long, unsigned long 
                bytesize = calcsize(longlongformat) 
                    
                f = file(name, "rb") 
                    
                filesize = os.path.getsize(name) 
                hash = filesize 
                    
                if filesize < 65536 * 2: 
                       return "SizeError" 
                 
                for x in range(65536/bytesize): 
                        buffer = f.read(bytesize) 
                        (l2, l1)= unpack(longlongformat, buffer) 
                        l_value = (long(l1) << 32) | long(l2) 
                        hash += l_value 
                        hash = hash & 0xFFFFFFFFFFFFFFFF #to remain as 64bit number  
                         
    
                f.seek(max(0,filesize-65536),0) 
                for x in range(65536/bytesize): 
                        buffer = f.read(bytesize) 
                        (l2, l1) = unpack(longlongformat, buffer) 
                        l_value = (long(l1) << 32) | long(l2) 
                        hash += l_value 
                        hash = hash & 0xFFFFFFFFFFFFFFFF 
                 
                f.close() 
                returnedhash =  "%016x" % hash 
                return returnedhash 
    
      except(IOError): 
                os.system('kdialog --error "Input/Output error while reading file hash"')
                return "IOError"

# ================== Main program ========================

server = ServerProxy("http://www.opensubtitles.org/xml-rpc")
peli = argv[1]

try:
    myhash = hashFile(peli)
    size = os.path.getsize(peli)
    session =  server.LogIn("","","en","python")
    
    token = session["token"]
    
    searchlist = []
    searchlist.append({'sublanguageid':'eng','moviehash':myhash,'moviebytesize':str(size)})
    
    moviesList = server.SearchSubtitles(token, searchlist)
    if moviesList['data']:
		mindex = 0
		kdialog_items = ''
		for item in moviesList['data']:
			kdialog_items = kdialog_items + '"' + str(mindex) + '" "' + item['SubFileName'] + '" '
			mindex = mindex + 1
	
		resp = os.popen('kdialog --geometry 400x200 --menu "Select subtitle" ' + kdialog_items).readline()
		subFileName = os.path.basename(peli)[:-3] + moviesList['data'][int(resp)]['SubFileName'][-3:]
		subDirName = os.path.dirname(peli)
		subURL = moviesList['data'][int(resp)]['SubDownloadLink']
		response = os.system('wget -O - ' + subURL + ' | gunzip  > "' + subDirName + '/' + subFileName + '"' )
		print 'wget -O - ' + subURL + ' | gunzip  > "' + subDirName + '/' + subFileName + '"' 
		if response != 0:
			os.system('kdialog --error "An error ocurred downloading or writing the subtitle"')
		
    else:
		os.system('kdialog --error "No subtitles found"')
    
    server.Logout(session["token"])
except Error, v:
    os.system('kdialog --error "An error ocurred"')



