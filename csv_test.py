# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 15:21:53 2019

@author: Will
"""

import csv


file = open('1856039.csv')
reader = csv.reader(file)
headers = []
count = 0
by_date = {}
for line in reader:
    count+=1
    if count == 1:
        headers = line
        #print(headers)
        continue
    else:
        data = {}
        for i in range(len(headers)):
            data[headers[i]] = line[i]
        by_date[line[5]] = data
date = 0
while True:
    date = input("ENTER A DATE: ")
    if date == 'quit':
        break
    print("The temperature was: " + str(by_date[date]['HLY-TEMP-NORMAL']))    