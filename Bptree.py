# -----------------------------------------------------------------------------
# xc2057
# Bptree.py
# B+ tree has insert, search, delete operation. 
# In our project, we only use insert and search.
# -----------------------------------------------------------------------------

from bisect import bisect_right,bisect_left
from tree_node import leaf_node, inter_node

class Bplus_Tree(object):
    def __init__(self, k):
        self.min_size = k
        self.max_size = 2*k-1
        self.root = leaf_node(self.min_size)

    def _search(self, key, node):
        output = None
        if(node.is_leaf()):   # leaf node
            for k_v in node.node_set:
                if(k_v[0] == key): output = k_v[1]  # output is a point array: [point1, point2], this can handle rep key issue.
        else:
            i = bisect_right(node.key_set, key)
            pointer = node.pointer_set[i]
            output = self._search(key, pointer)
        return output

    def search(self, key):
        # For terminal, print the search result
        node = self.root
        output = self._search(key, node)
        return output
    
    def leaf_insert(self, key, value, node):
        if(node.node_set == []):
            node.node_set.append((key, [value]))
        else:
            for i in range(0, len(node.node_set)):
                if(node.node_set[i][0] >= key): break
            if(node.node_set[i][0] > key):
                node.node_set.insert(i, (key, [value]))
            elif(node.node_set[i][0] < key):
                node.node_set.insert(i+1, (key, [value]))
            else:  # node.node_set[i][0] == key
                node.node_set[i][1].append(value)
    
    def leaf_split(self, node):
        mid = self.min_size
        new_node = leaf_node(self.min_size)
        new_node.node_set = node.node_set[mid:]
        node.node_set = node.node_set[:mid]
        new_key = new_node.node_set[0][0]
        new_node.brother = node.brother
        node.brother = new_node
        if(node.is_root()):
            newroot = inter_node(self.min_size)
            newroot.key_set.append(new_key)
            newroot.pointer_set = [node, new_node]
            node.parent = newroot
            new_node.parent = newroot
            self.root = newroot
        else:
            par = node.parent
            insert_loc = bisect_right(par.key_set, new_key)
            par.key_set.insert(insert_loc, new_key)
            par.pointer_set.insert(insert_loc+1, new_node)
            new_node.parent = par

    def inter_split(self, node):
        mid = self.min_size
        new_key = node.key_set[mid-1]
        new_node = inter_node(self.min_size)
        new_node.key_set = node.key_set[mid:]
        node.key_set = node.key_set[:mid-1]
        new_node.pointer_set = node.pointer_set[mid:]
        node.pointer_set = node.pointer_set[:mid]
        for p in new_node.pointer_set:
            p.parent = new_node
        if(node.is_root()):
            newroot = inter_node(self.min_size)
            newroot.key_set.append(new_key)
            newroot.pointer_set = [node, new_node]
            node.parent = newroot
            new_node.parent = newroot
            self.root = newroot
        else:
            par = node.parent
            insert_loc = bisect_right(par.key_set, new_key)
            par.key_set.insert(insert_loc, new_key)
            par.pointer_set.insert(insert_loc+1, new_node)
            new_node.parent = par
    
    def _insert(self, key, value, node):
        if(node.is_leaf()):
            self.leaf_insert(key, value, node)
            if(node.is_full()):
                self.leaf_split(node)
        else:
            i = bisect_right(node.key_set, key)
            pointer = node.pointer_set[i]
            self._insert(key, value, pointer)
            if(node.is_full()):
                self.inter_split(node)
    
    def insert(self, key, value):
        node = self.root
        self._insert(key, value, node)
    
    def key_remove(self, key, node):
        for k_v in node.node_set:
            if(k_v[0] == key): break
        if(k_v[0] == key):
            node.node_set.remove(k_v)
    
    def left_borrow(self, node, i, pointer, left_pointer):
        if(pointer.is_leaf()):
            borrow_k_v = left_pointer.node_set[-1]
            left_pointer.node_set.remove(borrow_k_v)
            pointer.node_set.insert(0, borrow_k_v)
            node.key_set[i-1] = pointer.find_min()
        else:
            borrow_p = left_pointer.pointer_set[-1]
            del left_pointer.pointer_set[-1]
            del left_pointer.key_set[-1]
            new_key = pointer.pointer_set[0].find_min()
            pointer.pointer_set.insert(0, borrow_p)
            pointer.key_set.insert(0, new_key)
            node.key_set[i-1] = pointer.find_min()
    
    def right_borrow(self, node, i, pointer, right_pointer):
        if(pointer.is_leaf()):
            borrow_k_v = right_pointer.node_set[0]
            right_pointer.node_set.remove(borrow_k_v)
            pointer.node_set.insert(self.max_size+1, borrow_k_v)
            node.key_set[i] = right_pointer.find_min()
        else:
            borrow_p = right_pointer.pointer_set[0]
            del right_pointer.pointer_set[0]
            del right_pointer.key_set[0]
            new_key = borrow_p.find_min()
            pointer.pointer_set.insert(self.max_size+1, borrow_p)
            pointer.key_set.insert(self.max_size+1, new_key)
            node.key_set[i] = right_pointer.find_min()
    
    def left_merge(self, node, i, pointer, left_pointer):
        if(pointer.is_leaf()):
            left_pointer.node_set = left_pointer.node_set + pointer.node_set
            left_pointer.brother = pointer.brother
        else:
            left_pointer.key_set = left_pointer.key_set + [pointer.pointer_set[0].find_min()] + pointer.key_set
            left_pointer.pointer_set = left_pointer.pointer_set + pointer.pointer_set
        del node.key_set[i-1]
        del node.pointer_set[i]
    
    def right_merge(self, node, i, pointer, right_pointer):
        if(pointer.is_leaf()):
            pointer.node_set = pointer.node_set + right_pointer.node_set
            pointer.brother = right_pointer.brother
        else:
            pointer.key_set = pointer.key_set + [right_pointer.pointer_set[0].find_min()] + right_pointer.key_set
            pointer.pointer_set = pointer.pointer_set + right_pointer.pointer_set
        del node.key_set[i]
        del node.pointer_set[i+1]         
 
    def _delete(self, key, node):
        if(node.is_leaf()):
            self.key_remove(key, node)
        else:
            i = bisect_right(node.key_set, key)
            pointer = node.pointer_set[i]
            self._delete(key, pointer)
            if(pointer.is_empty()):
                left_pointer = right_pointer = None
                #  Load child node's left/right brother
                if(i > 0 and node.pointer_set[i-1].size() > self.min_size): 
                    left_pointer = node.pointer_set[i-1]
                    self.left_borrow(node, i, pointer, left_pointer)
                elif(i < node.size()-1 and node.pointer_set[i+1].size() > self.min_size): 
                    right_pointer = node.pointer_set[i+1]
                    self.right_borrow(node, i, pointer, right_pointer)
                else:
                    if(i > 0):
                        left_pointer = node.pointer_set[i-1]
                        self.left_merge(node, i, pointer, left_pointer)
                    else:
                        right_pointer = node.pointer_set[i+1]
                        self.right_merge(node, i, pointer, right_pointer)
    
    def root_update(self, root):
        if(root.is_leaf() == False and root.size() == 1):
            root = root.pointer_set[0]
            root.parent = None
        return root
    
    def delete(self, key):
        node = self.root
        self._delete(key, node)
        self.root = self.root_update(node)
    
    def _leaf_localization(self, key, node):
        if(node.is_leaf()):   # leaf node
            return node
        else:
            i = bisect_right(node.key_set, key)
            pointer = node.pointer_set[i]
            return self._leaf_localization(key, pointer)

    # output the key-value lower than one key.  <
    def range_search_low(self, key):
        output = []
        tag_node = self._leaf_localization(key, self.root)
        start_node = self.root
        while(start_node.is_leaf() == False):
            start_node = start_node.pointer_set[0]
        node = start_node
        while(node != tag_node):
            for k_v in node.node_set:
                for v in k_v[1]: output.append(v)
            node = node.brother
        for k_v in node.node_set:
            if(k_v[0] >= key): break
            for v in k_v[1]: output.append(v)
        return output
    
    # output the key-value greater than one key.   >
    def range_search_up(self, key):
        output = []
        tag_node = self._leaf_localization(key, self.root)
        for k_v in tag_node.node_set:
            if(k_v[0] > key):
                for v in k_v[1]: output.append(v)
        node = tag_node.brother
        while(node != None):
            for k_v in node.node_set:
                for v in k_v[1]: output.append(v)
            node = node.brother
        return output
    
    def index_sort(self):
        output = []
        node = self.root
        while(node.is_leaf() == False):
            node = node.pointer_set[0]
        while(node != None):
            for k_v in node.node_set:
                output += k_v[1]
            node = node.brother
        return output
    
