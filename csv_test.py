# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 15:21:53 2019

@author: Will
"""

import csv,sys

file = open('1856039.csv')
reader = csv.reader(file)
headers = []
count = 0
by_date = {}
temps = {}
dates = []
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
        temps[line[5]] = data['HLY-TEMP-NORMAL']
        dates.append(line[5])
outfile = open('temps.txt', 'w')
sys.stdout = outfile

for i in range(len(dates) - 10):
    toprint = ''
    if i % 10 == 0:
        for j in range(9):
            toprint += str(temps[dates[i + j]]) + " "
        toprint += str(temps[dates[i+9]])
        print(toprint)
outfile = open('test_data.txt', 'w')
sys.stdout = outfile
for i in range(len(dates) - 10):
    toprint = ''
    for j in range(9):
        toprint += str(temps[dates[i + j]]) + " "
    toprint += str(temps[dates[i+9]])
    print(toprint)
        