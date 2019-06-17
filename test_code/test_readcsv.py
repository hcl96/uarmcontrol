# -*- coding: utf-8 -*-
'''
Created on Thu Apr  4 23:31:16 2019

@author: xumw1
'''

import csv

filename = 'fullprogram_out_config.csv'

#filename = 'test.csv'


def getrow(filename):
    # read csv file using generator
    with open(filename) as csvfile:
        datareader = csv.reader(csvfile)
        for row in datareader:
            yield row


for item in getrow(filename):
    print(item)
