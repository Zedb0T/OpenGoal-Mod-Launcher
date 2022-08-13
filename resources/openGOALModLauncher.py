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
import shutil

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

def process_exists(process_name):
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    # use buildin check_output right away
    output = subprocess.check_output(call).decode()
    # check in last line for process name
    last_line = output.strip().split('\r\n')[-1]
    # because Fail message could be translated
    return last_line.lower().startswith(process_name.lower())

def try_kill_process(process_name):
	if process_exists(process_name):
		os.system("taskkill /f /im " + process_name)

def try_remove_file(file):
	if exists(file):
		os.remove(file)

def try_remove_dir(dir):
	if exists(dir):
		shutil.rmtree(dir)

#start of update check method
#Github API Call
PARAMS = {'address':"yolo"} 
r = requests.get(url = URL, params = PARAMS)  
InstallDir = os.getenv('APPDATA') + "\\OpenGOAL-"+ MOD_NAME
AppdataPATH = os.getenv('APPDATA')
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

	#Close Gk and goalc if they were open.
	try_kill_process("gk.exe")
	try_kill_process("goalc.exe")

	#download update from github
	# Create a new directory because it does not exist 
	print("Downloading update")
	if not os.path.exists(InstallDir):
	  os.makedirs(InstallDir)
	  print("The new directory is created!")
	  
	urllib.request.urlretrieve(LatestRelAssetsURL, InstallDir + "/updateDATA.zip")
	print("Done downloading")
	
	#backup iso_data to avoid re-extraction
	if exists(InstallDir + "/data/iso_data"):
		shutil.move(InstallDir + "/data/iso_data", InstallDir + "/backup/iso_data")
	
	#delete any previous installation
	print("Removing previous installation " + InstallDir)
	try_remove_dir(InstallDir + "/data")
	try_remove_file(InstallDir + "/gk.exe")
	try_remove_file(InstallDir + "/goalc.exe")
	try_remove_file(InstallDir + "/extractor.exe")

	#restore backed up iso_data to avoid re-extraction
	if exists(InstallDir + "/backup/iso_data"):
		shutil.move(InstallDir + "/backup/iso_data", InstallDir + "/data/iso_data")
		try_remove_dir(InstallDir + "/backup")
	
	#extract update
	print("Extracting update")
	with zipfile.ZipFile(InstallDir + "/updateDATA.zip","r") as zip_ref:
		zip_ref.extractall(InstallDir)

	#delete the update archive
	try_remove_file(InstallDir + "/updateDATA.zip")

	#if extractOnUpdate is True, check their ISO_DATA folder

	#if ISO_DATA has content, store this path to pass to the extractor
	if (exists(AppdataPATH + "\OpenGOAL-Launcher\data\iso_data\jak1\Z6TAIL.DUP")):
		iso_path = AppdataPATH + "\OpenGOAL-Launcher\data\iso_data\jak1"
	else:
		#if ISO_DATA is empty, prompt for their ISO and store its path.
		root = tk.Tk()
		print("Please select your iso.")
		root.title("Select ISO")
		root.geometry('1x1')
		iso_path = filedialog.askopenfilename()
		root.destroy()

	print("Running extractor.exe with ISO: " + iso_path)
	subprocess.Popen("\""+InstallDir +"\extractor.exe""\""""" -f """ + "\""""+ iso_path+"\"""")

else:
	#if we dont need to update, then close any open instances of the game and just launch it

	#Close Gk and goalc if they were open.
	try_kill_process("gk.exe")
	try_kill_process("goalc.exe")

	time.sleep(1)
	print(GKCOMMANDLINElist)
	subprocess.Popen(GKCOMMANDLINElist)