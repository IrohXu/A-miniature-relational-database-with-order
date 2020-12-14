import re
import time

class node(object):
    def __init__(self, key, index):
        """
        Node in the hashing
        """
        self.key = key
        self.pointer_index = index     #  The index will localize to the array(can be consider as a pointer)
        self.next = None

class hashing(object):
    def __init__(self, B, data):
        self.size = B
        self.array = data
        self.dict = {}
        for i in range(0, self.size): self.dict[i] = None
    
    def length(self):
        return len(self.array)

    def _insert(self, key, value):
        dict_key = key%self.size
        if(self.dict[dict_key] is None):
            self.dict[dict_key] = node(key, value)
        else:
            new_node = node(key, value)
            new_node.next = self.dict[dict_key]
            self.dict[dict_key] = new_node
    
    def insert(self, key, value):
        self._insert(key, value)

    def _search(self, key):
        dict_key = key%self.size
        head = self.dict[dict_key]
        output = []
        while(head != None):
            if(head.key == key):
                output.append(head.pointer_index)
            head = head.next
        return output
    
    def search(self, key):
        return self._search(key)

    def _delete(self, key):
        dict_key = key%self.size
        head = self.dict[dict_key]
        while(head != None and head.key == key):
            self.dict[dict_key] = head.next
            head = head.next
        if(head != None):
            while(head.next != None):
                if(head.next.key == key):
                    head.next = head.next.next
                else:
                    head = head.next
    
    def delete(self, key):
        self._delete(key)
    
    def visualization(self):
        for dict_key in self.dict:
            temp_key_value = []
            head = self.dict[dict_key]
            while(head != None):
                temp_key_value.append((head.key, head.pointer_index))
                head = head.next
            print(str(dict_key)+':'+str(temp_key_value))
    
    def search_all(self):
        print("key|value")
        for dict_key in self.dict:
            head = self.dict[dict_key]
            while(head != None):
                print(str(self.array[head.pointer_index][0]) + "|" + str(self.array[head.pointer_index][1]))
                head = head.next
    
    def load_table(self, table_path):
        fd = open(table_path)
        fd.readline()    # first line is key|value, do not need it
        i = 0
        while(True):
            line = fd.readline()
            if(line == ""):
                break
            info = line.split('|')
            self.array.append(info)
            self.insert(int(info[0]), i)
            i+=1

if __name__ == '__main__':
    ticks = time.time()
    h = hashing(10, [])
    input_table = './myIndex.txt'
    h.load_table(input_table)
    h.visualization()

    print('\nTotal time used include insert data and exec commands is',(time.time()-ticks))
    # h.search_all()    # Print all
