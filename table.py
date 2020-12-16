# -----------------------------------------------------------------------------
# xc2057
# table.py
# including inputfromfile, output, outputtofile
# -----------------------------------------------------------------------------

import re
import os

class Table():
    def __init__(self, column):
        self.column = column   # column should be a list
        self.data = []   # data in the table should be list
        self.size = 0
        self.hash = {}
        self.bptree = {}
        for c in column:
            self.hash[c] = None
            self.bptree[c] = None
    
    def insert(self, row):
        self.data.append(row)
        self.size += 1

# COLUMN_PATTERN = re.compile(r'\S+') 

def inputfromfile(table_path):
    fd = open(table_path)
    first_line = fd.readline().strip('\n').upper()    # first line is the column name divided by '|'
    column = first_line.split('|')
    table = Table(column)
    while(True):
        line = fd.readline().strip('\n')
        if(line == ""): break
        info = line.split('|')
        # change all info in the table array to int
        table.insert([int(x) for x in info])
    return table

def outputtable(table):  # table is a table class
    standardout = '|'.join(table.column)
    print(standardout)
    for info in table.data:
        if info == None: continue
        standardout = '|'.join([str(x) for x in info])
        print(standardout)

def outputtofile(table, output_path):  # table is a table class
    if(os.path.exists(output_path)):
        os.remove(output_path)
    with open(output_path ,'w') as f:
        column = '|'.join(table.column)
        f.write(column)
        for info in table.data:
            if info == None: continue
            data = '|'.join([str(x) for x in info])
            f.write("\n"+data)
      
