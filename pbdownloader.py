#!/opt/local/bin/python

# Basic/dumb script for downloading the contents of your photobucket account
# 1. Select all the files you want to download in the WebUI.  If you select one in an album, 
#       it'll give you a "select all" button for the rest.  You can select files in multiple albums.
# 2. "Link" button at the bottom
# 3. Copy the "Direct" section, and paste it into a plaintext file
# 4. run this script with that file as the argument (./pbdownloader.py myimages.txt)

import os
import requests
import sys


file_list_name = sys.argv[1]
base_download_dir = os.getcwd()
fh = open(file_list_name)
for line in fh.readlines():
    if 'photobucket.com' not in line:
        print("Not a photobucket URL: %s" % line)
        continue
    line = line.rstrip()
    splitline = line.split('/')
    folder_name = splitline[-2:-1][0]
    file_name = splitline[-1:][0]
    # handle base folder
    if len(splitline) == 7:
        folder_name = 'main_album_bucket'
    if not os.path.exists(base_download_dir + '/' + folder_name):
        print("Creating folder for album: %s" % folder_name)
        os.mkdir(folder_name)
   
    print("Downloading %s" % line) 
    dl_file = requests.get(line, headers={'referer': 'http://s.photobucket.com/'})
    if dl_file.status_code != 200:
        print("Error %d downloading URL: %s" % (dl_file.status_code, line))
        continue
    dl_fh = open(folder_name + '/' + file_name, 'wb')
    dl_fh.write(dl_file.content)
    dl_fh.close()


