# python-version-2.O
updated
# what's new in 2.o
# Match statement
```python
def check_match(string):
    check_list=["abc","xyz","none","etc"]
    for i in check_list:
        match string:
            case 'abc':
                print("string is abc")
            case 'xyz':
                print("string is xyz")
            case _:
                print("string is not abc and xyz")
```
# Iter() 
One useful application of the second form of iter() is to build a block-reader. 
```python
from functools import partial
#One useful application of the second form of iter() is to build a block-reader. 
# For example, reading fixed-width blocks from a binary database file until the end of file is reached:
with open("/home/hiader/Desktop/code/fruit_data_with_colors.txt","rb") as f:
    for block in iter(partial(f.read,64),b''):
        print(block)
print(locals())
print(globals())
```
