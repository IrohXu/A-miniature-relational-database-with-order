# -----------------------------------------------------------------------------
# xc2057
# tree_node.py
# -----------------------------------------------------------------------------

'''
Tree node class in B+ Tree
'''

class leaf_node(object):
    def __init__(self, k):
        """
        Node of the leaf in B+ Tree
        """
        self.min_size = k
        self.max_size = 2*k-1
        self.node_set = []   # As their might have rep key, I use a tuple (key, []) to store pointer to array 
        self.brother = None
        self.parent = None
    
    def is_leaf(self): return True
    
    def is_root(self):
        if(self.parent == None): return True
        return False
    
    def is_full(self):
        if(len(self.node_set) > self.max_size): return True
        else: return False
    
    def is_empty(self):
        if(len(self.node_set) < self.min_size): return True
        else: return False
    
    def find_min(self):
        if(self.node_set == []): return None
        return min(self.node_set)[0]
    
    def find_max(self):
        if(self.node_set == []): return None
        return max(self.node_set)[0]
    
    def size(self): return len(self.node_set)

class inter_node(object):
    def __init__(self, k):
        """
        Node of the non-leaf in B+ Tree
        """
        self.min_size = k
        self.max_size = 2*k-1
        self.key_set = []
        self.pointer_set = []
        self.parent = None
    
    def is_leaf(self):  return False
    
    def is_root(self):
        if(self.parent == None): return True
        return False
    
    def is_full(self):
        if(len(self.pointer_set) > self.max_size): return True
        else: return False
    
    def is_empty(self):
        if(len(self.pointer_set) < self.min_size): return True
        else: return False
    
    def size(self): return len(self.pointer_set)
    
    def find_min(self):
        if(self.key_set == []): return None
        return min(self.key_set)
    
    def find_max(self):
        if(self.key_set == []): return None
        return max(self.key_set)