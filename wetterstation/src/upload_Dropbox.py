#!/usr/bin/env python
from datetime import date, timedelta

import dropbox, keys


dbx = dropbox.Dropbox(keys.DROPBOX_TOKEN)

yesterday = date.today() - timedelta(1) 

filename = yesterday.strftime("%Y%m%d") +  '.txt'
file = keys.DIR + filename
target = '/' + filename

with open(file, 'rb') as f:
        dbx.files_upload(f.read(), target)