#!/usr/bin/env python
import dropbox, keys
from datetime import date, timedelta

dbx = dropbox.Dropbox(keys.DROPBOX_TOKEN)

yesterday = date.today() - timedelta(1) 

filename = yesterday.strftime("%Y%m%d") +  '.txt'
file = keys.DIR + filename
target = '/' + filename

with open(file, 'rb') as f:
        dbx.files_upload(f.read(), target)