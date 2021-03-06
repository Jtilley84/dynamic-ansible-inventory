#!/usr/bin/env python 

# Super simple python script to convert a server inventory csv into a Ansible
# inventory sorted by a specific column. Just add your .csv to the project folder,
# update the two variables listed below and you're in business!

''' import our required modules '''
import csv 
import os
import datetime
import shutil 

''' update this to your .ini '''
your_ini = 'test.ini'

''' your server inventory spreadsheet '''
your_csv = 'example.csv'

''' replace example.csv with your server inventory '''
f = csv.reader(file(your_csv))

''' set our variable that we will be sorting the csv out with '''
old_location = ''

''' Check to see if our inventory file already exists '''
inventory_exists = os.path.isfile('test.ini')
if( inventory_exists == True ):

    source = os.listdir('./')

    ''' Create our backups folder if it doesn't exist '''
    if not os.path.exists('./backups'):
        os.makedirs('backups', mode=0755)

    destination = './backups/'
    for files in source:

        ''' Do we already have an Ansible inventory in the folder? '''
        if files.endswith('.ini'):

            ''' create our backup file and attach a timestamp '''
            timestamp = datetime.datetime.now()
            backup = str(timestamp) + '--' + files
            os.rename(files, backup)

            ''' copy it to our backups folder, then delete the temp '''
            shutil.copy(backup, destination)
            os.remove(backup)

''' iterate through each line, skipping the headers '''
firstLine = True
for row in f:
    if firstLine:
        firstLine = False
        continue 

    ''' read our new location '''
    new_location = row[4]

    ''' If we have a new server location, write a proper header '''
    if( new_location != old_location ):
        location_header = '['+ new_location + ']'

        ''' swap test.ini with your Ansible inventory file '''
        inventory = open(your_ini, 'a')
        inventory.write('\n' + location_header + '\n')
        ip = row[1]
        hostname = row[0]
        inventory.write(ip + '  ansible_hostname='+hostname+'\n')

    else:
        ''' otherwise, keep adding new servers to this location '''
        inventory = open(your_ini, 'a')
        ip = row[1]
        hostname = row[0]
        inventory.write(ip + '  ansible_hostname='+hostname+'\n')

    ''' update our old location value to check the next row '''
    old_location = new_location

inventory.close()

