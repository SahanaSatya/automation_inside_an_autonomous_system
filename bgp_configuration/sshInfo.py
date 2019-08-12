import csv
import os
def parse_file(file_name):
    if os.path.isfile(file_name):
        devices = []
        with open (file_name) as csvfile1:
            reader = csv.reader(csvfile1)
            for row in reader:
                if row:
                    if row != None:
                        devices.append({row[0]:row[1],row[2]:row[3],row[4]:row[5],row[6]:row[7],row[8]:row[9]})
        return devices
    else:
        return"File not present"
