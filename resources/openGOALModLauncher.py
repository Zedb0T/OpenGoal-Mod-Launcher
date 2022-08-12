# -*- coding: utf-8 -*-
"""
Created on Fri Aug 12 06:51:37 2022

@author: Zed
"""
import tkinter as tk
from tkinter import filedialog
import os
import subprocess
import sys
import time
from os.path import exists
import requests
import json
import pathlib
from datetime import datetime
import urllib.request
import zipfile


#SET THESE
URL="https://api.github.com/repos/zedb0t/OpenGoal-CheckpointRandomizer/releases"
EXTRACT_ON_UPDATE="true"            
FILE_DATE_TO_CHECK="gk.exe"
UPDATE_FILE_EXTENTION=".zip"
MOD_NAME="REMEBERTTOCHANGETHIS"


# Folder where script is placed, It looks in this for the Exectuable
if getattr(sys, 'frozen', False):
    InstallDir = os.path.dirname(os.path.realpath(sys.executable))
elif __file__:
    InstallDir = os.path.dirname(__file__)

extractOnUpdate = bool(str(EXTRACT_ON_UPDATE).replace("t","T").replace("f", "F"))
ExecutableName = str(FILE_DATE_TO_CHECK) # Executable we're checking the 'modified' time of
FileExt = str(UPDATE_FILE_EXTENTION) # content_type of the .deb release is also "application\zip", so rely on file ext
FileIdent = "" # If we ever get to multiple .zip files in a release, include other identifying information from the name (e.g. "windows-x64")


#start of update check method
#Github API Call
PARAMS = {'address':"yolo"} 
r = requests.get(url = URL, params = PARAMS)  
InstallDir = os.getenv('APPDATA') + "\\OpenGOAL-"+ MOD_NAME
extraGKCommand = "-proj-path "+os.getenv('APPDATA') + "\\OpenGOAL-"+MOD_NAME+"\\data "
PATHTOGK = InstallDir +"\gk.exe "+extraGKCommand+"-boot -fakeiso -v"
GKCOMMANDLINElist = PATHTOGK.split()
#store Latest Release and check our local date too.
LatestRel = datetime.strptime(json.loads(json.dumps(r.json()))[0].get("published_at").replace("T"," ").replace("Z",""),'%Y-%m-%d %H:%M:%S')
LatestRelAssetsURL = (json.loads(json.dumps(requests.get(url = json.loads(json.dumps(r.json()))[0].get("assets_url"), params = PARAMS).json())))[0].get("browser_download_url")
LastWrite = datetime(2020, 5, 17)
if (exists(InstallDir + "/" + ExecutableName)):
	LastWrite = datetime.utcfromtimestamp( pathlib.Path(InstallDir + "/" + ExecutableName).stat().st_mtime)
	

needUpdate = bool((LastWrite < LatestRel))

print("Currently installed version created on: " + LastWrite.strftime('%Y-%m-%d %H:%M:%S'))
print("Newest version created on: " + LatestRel.strftime('%Y-%m-%d %H:%M:%S'))
print("Do we need to update? ")
print(needUpdate)

if (needUpdate):
#start the actual update method if needUpdate is true

#close current files so we can update them

#download update from github
	print("Downloading update")
	urllib.request.urlretrieve(LatestRelAssetsURL, InstallDir + "updateDATA.zip")
	print("Done downloading")
	
	print("Extracting update")
	

	with zipfile.ZipFile(InstallDir + "updateDATA.zip","r") as zip_ref:
		   zip_ref.extractall(InstallDir)


#extract update

#delete the update archive

#if extractOnUpdate is True, check their ISO_DATA folder

	if (exists("data\iso_data\jak1\Z6TAIL.DUP")):
		iso_path = "data\iso_data\jak1"



#if ISO_DATA is empty, prompt for their ISO and store its path.
	if (not (exists("data\iso_data\jak1\Z6TAIL.DUP"))):
		root = tk.Tk()
		iso_path = filedialog.askopenfilename()
		root.destroy()


#if ISO_DATA has content, store this path to pass to the extractor
	
	subprocess.Popen("\""+InstallDir +"\extractor.exe""\""""" -f """ + "\""""+ iso_path+"\"""")


#run extractor


#if we dont need to update, then close any open instances of the game and just launch it
if (not(needUpdate)):
	#Close Gk and goalc if they were open.
	print("If it errors below that is O.K.")
	subprocess.Popen("""taskkill /F /IM gk.exe""",shell=True)
	subprocess.Popen("""taskkill /F /IM goalc.exe""",shell=True)
	time.sleep(1)
	print(GKCOMMANDLINElist)
	subprocess.Popen(GKCOMMANDLINElist)






	