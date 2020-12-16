# -----------------------------------------------------------------------------
# xc2057
# operation.py
# -----------------------------------------------------------------------------


from table import Table
from hash import hashing
from Bptree import Bplus_Tree
import re

def find_index(key, tup):  # key might be a value in tuple, tup is a tuple.
    for i in range(0, len(tup)):
        if tup[i] == key: return i
    raise KeyError("No column name "+str(key)+" in table.")

def project(S, Clist):  # S is a table, Clist is a list of column name
    column_dist = {}
    for column_name in Clist: column_dist[column_name] = find_index(column_name, S.column)
    new_column = Clist
    table = Table(new_column)
    for row in S.data:
        if row == None: continue
        new_data = []
        for column_name in new_column:
            new_data.append(row[column_dist[column_name]])
        table.insert(new_data)
    return table

def compare(value1, cop, value2):
    if(cop == '<'):
        if(value1 < value2): return True
    elif(cop == '>'):   
        if(value1 > value2): return True
    elif(cop == '=='):   
        if(value1 == value2): return True
    elif(cop == '='):   
        if(value1 == value2): return True
    elif(cop == '>='):   
        if(value1 >= value2): return True
    elif(cop == '<='):   
        if(value1 <= value2): return True
    elif(cop == '!='):   
        if(value1 != value2): return True
    return False

def select(S, condition):
    pattern = re.compile(r'\S+')
    cop = re.compile(r'[><=!]+')
    condition_list = pattern.findall(condition)
    if(len(condition_list) == 1):  # no and/or
        cop_list = cop.findall(condition_list[0])
        if(len(cop_list) != 1): raise SyntaxError("Wrong condition setting.")
        comp = cop_list[0]
        if(comp not in ['<', '>', '==', '<=', '>=', '!=', '=']): raise SyntaxError("Wrong condition setting.")
        c = re.split(r'[><=!]+', condition_list[0])   # column or constant
        if(len(c) != 2):  raise SyntaxError("Wrong condition setting.")
        c1 = c[0]
        c2 = c[1]
        table = Table(S.column)
        if(c1 in S.column and c2 in S.column):
            c1_key = find_index(c1, S.column)
            c2_key = find_index(c2, S.column)
            for row in S.data:
                if(row == None): continue
                if(compare(row[c1_key], comp, row[c2_key])): table.insert(row)
        elif(c1 in S.column):  # c2 might be a constant
            c1_key = find_index(c1, S.column)
            c2 = int(c2)
            if(S.hash[c1] != None and comp in ['=', '==']):    # Use hash
                row_set = S.hash[c1].search(c2)
                for pointer in row_set:
                    table.insert(S.data[pointer])
            elif(S.bptree[c1] != None and comp in ['>', '>=', '<', '<=']):
                if(comp in ['>', '>=']):
                    row_set = S.bptree[c1].range_search_up(c2)
                    if(comp == '>='):
                        row_set = S.bptree[c1].search(c2) + row_set
                    for pointer in row_set:
                        table.insert(S.data[pointer])
                else: # comp in ['<', '<=']
                    row_set = S.bptree[c1].range_search_low(c2)
                    if(comp == '<='):
                        row_set = row_set + S.bptree[c1].search(c2)
                    for pointer in row_set:
                        table.insert(S.data[pointer])
            else:
                for row in S.data:
                    if(row == None): continue
                    if(compare(row[c1_key], comp, c2)): table.insert(row)
        elif(c2 in S.column):  # c2 might be a constant
            c2_key = find_index(c2, S.column)
            c1 = int(c1)
            if(S.hash[c2] != None and comp in ['=', '==']):   # Use hash
                row_set = S.hash[c2].search(c1)
                for pointer in row_set:
                    table.insert(S.data[pointer])
            elif(S.bptree[c2] != None and comp in ['>', '>=', '<', '<=']):
                if(comp in ['>', '>=']):
                    row_set = S.btree[c2].range_search_low(c1)
                    if(comp == '>='):
                        row_set = S.btree[c2].search(c1) + row_set
                    for pointer in row_set:
                        table.insert(S.data[pointer])
                else: # comp in ['<', '<=']
                    row_set = S.btree[c2].range_search_up(c1)
                    if(comp == '<='):
                        row_set = row_set + S.btree[c2].search(c1)
                    for pointer in row_set:
                        table.insert(S.data[pointer])
            else:
                for row in S.data:
                    if(row == None): continue
                    if(compare(c1, comp, row[c2_key])): table.insert(row)
        else:
            raise SyntaxError("Wrong condition setting.")
    else:
        raise SyntaxError("Wrong condition setting.")
    return table

def sort(S, C1):
    table = Table(S.column)  # The returned new table
    New_data = list(filter(None, S.data))  # delete the memory if there is any None value
    key = find_index(C1, S.column)
    if(S.bptree[C1] != None):
        row_set = S.bptree[C1].index_sort()
        for pointer in row_set:
            table.insert(S.data[pointer])
    else:
        New_data.sort(key = lambda elem: elem[key], reverse=False)
        table.data = New_data
        table.size = len(table.data)
    return table

def concat(R, S):
    if(R.column != S.column): raise SyntaxError("Wrong condition setting.")
    table = Table(R.column)  # The returned new
    for Rdata in R.data:
        if(Rdata == None): continue
        table.insert(Rdata)
    for Sdata in S.data:
        if(Sdata == None): continue
        table.insert(Sdata)
    return table

def column_sum(S, C1):
    key = find_index(C1, S.column)
    table = Table(['RESULT'])
    summ = 0
    for Sdata in S.data:
        if(Sdata == None): continue
        summ+=Sdata[key]
    table.insert([summ])
    return table

def column_avg(S, C1):
    key = find_index(C1, S.column)
    table = Table(['RESULT'])
    summ = 0
    num = 0
    for Sdata in S.data:
        if(Sdata == None): continue
        summ+=Sdata[key]
        num+=1
    if(num == 0):   table.insert([0])
    else:   table.insert([int(summ/num)])
    return table

def sumgroup(S, C1, Clist):
    group = {}
    column_dist = {}
    for column_name in Clist: column_dist[column_name] = find_index(column_name, S.column)
    for Sdata in S.data:
        group[tuple([Sdata[column_dist[column_name]] for column_name in Clist])] = 0
    key = find_index(C1, S.column)
    for Sdata in S.data:
        group[tuple([Sdata[column_dist[column_name]] for column_name in Clist])] += Sdata[key]
    table = Table(Clist+['RESULT'])
    for k in group:
        table.insert([i for i in k]+[group[k]])
    return table

def avggroup(S, C1, Clist):
    group = {}
    column_dist = {}
    for column_name in Clist: column_dist[column_name] = find_index(column_name, S.column)
    for Sdata in S.data:
        key = tuple([Sdata[column_dist[column_name]] for column_name in Clist])
        group[key] = [0,0]
    key = find_index(C1, S.column)
    for Sdata in S.data:
        group[tuple([Sdata[column_dist[column_name]] for column_name in Clist])][0] += Sdata[key]
        group[tuple([Sdata[column_dist[column_name]] for column_name in Clist])][1] += 1
    table = Table(Clist+['RESULT'])
    for k in group:
        table.insert([i for i in k]+[int(group[k][0]/group[k][1])])
    return table

def join(R, Rname, S, Sname, condition):
    cop = re.compile(r'[><=!]+')
    cop_list = cop.findall(condition)
    if(len(cop_list) != 1): raise SyntaxError("Wrong condition setting.")
    comp = cop_list[0]
    if(comp not in ['<', '>', '==', '<=', '>=', '!=', '=']): raise SyntaxError("Wrong condition setting.")
    c = re.split(r'[><=!]+', condition)   # column or constant
    if(len(c) != 2):  raise SyntaxError("Wrong condition setting.")
    c1 = c[0]
    c2 = c[1]

    table = Table([Rname + '_' + i for i in R.column] + [Sname + '_' +j for j in S.column])

    if(re.split(r'_', c1)[0] == Rname and re.split(r'_', c2)[0] == Sname):
        c1_key = find_index(re.split(r'_', c1)[1], R.column)
        c2_key = find_index(re.split(r'_', c2)[1], S.column)

        for Rdata in R.data:
            if(Rdata == None): continue
            for Sdata in S.data:
                if(Sdata == None): continue
                if(compare(Rdata[c1_key], comp, Sdata[c2_key])):
                    table.insert(Rdata + Sdata)
    elif(re.split(r'_', c1)[0] == Sname and re.split(r'_', c2)[0] == Rname):
        c1_key = find_index(re.split(r'_', c1)[1], S.column)
        c2_key = find_index(re.split(r'_', c2)[1], R.column)

        for Rdata in R.data:
            if(Rdata == None): continue
            for Sdata in S.data:
                if(Sdata == None): continue
                if(compare(Sdata[c1_key], comp, Rdata[c2_key])):
                    table.insert(Rdata + Sdata)
    else:
        raise SyntaxError("Wrong condition setting.")
    return table

def movsum(S, C1, k):
    table = Table(['RESULT'])
    key = find_index(C1, S.column)
    sum_list = [0 for i in range(0, k)]
    i = 0
    for Sdata in S.data:
        if(Sdata == None): continue
        if(i < k): 
            sum_list[i] = Sdata[key]
        else:
            sum_list.pop(0)
            sum_list.append(Sdata[key])
        i += 1
        table.insert([sum(sum_list)])
    return table

def movavg(S, C1, k):
    table = Table(['RESULT'])
    key = find_index(C1, S.column)
    sum_list = [0 for i in range(0, k)]
    i = 0
    for Sdata in S.data:
        if(Sdata == None): continue
        if(i < k): 
            sum_list[i] = Sdata[key]
            table.insert([int(sum(sum_list)/(i+1))])
        else:
            sum_list.pop(0)
            sum_list.append(Sdata[key])
            table.insert([int(sum(sum_list)/k)])
        i += 1
    return table

def Hash(R, C1):
    R.hash[C1] = hashing(R.size)
    key = find_index(C1, R.column)
    for Ri in range(0, R.size):
        R.hash[C1].insert(R.data[Ri][key], Ri)

def Btree(R, C1):
    R.bptree[C1] = Bplus_Tree(53)   # TEMP use 23 here, you can change it.
    key = find_index(C1, R.column)
    for Ri in range(0, R.size):
        R.bptree[C1].insert(R.data[Ri][key], Ri)
