from ast import Return
from tabnanny import check
from urllib3 import Retry

class balanced_tree:
    def __init__(self,value):
        self.value = value
        self.left = None
        self.right = None
    def insert(self,value):
        if self.value > value:
            if self.left is None:
                self.left = balanced_tree(value)
            else:
                self.left.insert(value)
        elif self.value < value:
            if self.right is None:
                self.right = balanced_tree(value)
            else:
                self.right.insert(value)
        else:
            print("value already exists")
    
   # Mian function
   # for finding the shortest path between two nodes
   # in a binary search tree 
    def shortest_path(self,value1,vlaue2,counter,check_1):
        if self.value == value1:
            check_1 = True
            
            print("true",counter)
        if self.value == vlaue2:
            print("flase",counter)
            return counter
        if self.left is not None:
            if check_1 == True:
                self.left.shortest_path(value1,vlaue2,counter+1,check_1)
            else:
                self.left.shortest_path(value1,vlaue2,counter,check_1)
        if self.right is not None:
            if check_1 == True:
                self.right.shortest_path(value1,vlaue2,counter+1,check_1)
            else:
                self.right.shortest_path(value1,vlaue2,counter,check_1)
            
        
if __name__=="__main__":
    bst=balanced_tree(1)
    bst.insert(10)
    bst.insert(8)
    bst.insert(4)
    bst.insert(9)
    bst.insert(12)
    bst.insert(11)
    print(bst.shortest_path(1,12,0,False))
  