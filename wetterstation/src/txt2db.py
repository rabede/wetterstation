'''
Created on 27.12.2016

@author: bell
'''
import sqlite3
import os
import openpyxl
from math import isclose

conn = sqlite3.connect('wetter.sqlite')
cur = conn.cursor()
data_dir = "../data"

def save_data(cur, data):
    try:
        cur.execute('''INSERT OR IGNORE into wetter (timestamp, temperatur, humidity, windspeed, downfall, rain)       
                       VALUES (?,?,?,?,?,?)''',     (data[0], data[1], data[2], data[3], data[4], data[5]))
    except:
        print('Error: ', data)

def check_data(data):
    try:
        if not (-20 > float(data[1]) ): # or (0 > float(data[2]) > 100) or (0 > float(data[3]) > 50) or (0 > float(data[4]) > 20):
            print(data[1])
    except:
        print(data)  

#importformat ['2015-02-15 07:12', '-2.3', '95.0', '0.0', 0, '0'] von raspberry:
def get_wetterpi(file):
        text = open(file)
        for line in text:
            cleanline = line.strip("[]\n").replace("'", "")
            data = cleanline.split(",")
#            check_data(data)
            save_data(cur, data)

def get_google(file):
    data = [None,0.0,0.0,0,0.0, None]
    old_data = data[:]
    wb = openpyxl.load_workbook(file)
    sheet = wb.get_sheet_by_name('Tabellenblatt1')
    for row in range(2, sheet.max_row + 1):
        if sheet.cell(row = row, column = 1).value == None:
            continue
        for col in range(6):
            data[col] = sheet.cell(row = row, column =  col+1).value
            
        data[1] = float(data[1])
            
        if data[5] == 'ja':
            data[5] = 1
        else:
            data[5] = 0
        
        if not old_data[0] is None and not isclose(data[1], old_data[1], abs_tol=1):
            print(data[0], data[1], old_data[0], old_data[1])
        else: 
            old_data = data[:]
        #save_data(cur, data)
        

def loop_dir(dir):
    ''' Loop over the files in the working directory.'''
    for file in os.listdir('.'):
        if file.endswith('.txt'):
            get_wetterpi(file)
        elif file.endswith('.xlsx'):
            pass
            #get_google(file)
        else:
            continue
        os.rename(file, file + '.read')
        conn.commit()

os.chdir(data_dir)
loop_dir(data_dir)

conn.commit()
conn.close()
