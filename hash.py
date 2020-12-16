# -----------------------------------------------------------------------------
# xc2057
# hash.py
# hash has insert, search, delete operation. 
# In our project, we only use insert and search.
# -----------------------------------------------------------------------------

class node(object):
    def __init__(self, key, index):
        """
        Node in the hashing
        """
        self.key = key
        self.pointer_index = index     #  The index will localize to the array(can be consider as a pointer)
        self.next = None

class hashing(object):
    def __init__(self, B):
        self.size = B
        self.dict = {}
        for i in range(0, self.size): self.dict[i] = None

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
