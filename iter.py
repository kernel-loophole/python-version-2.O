from functools import partial
#One useful application of the second form of iter() is to build a block-reader. 
# For example, reading fixed-width blocks from a binary database file until the end of file is reached:
with open("/home/hiader/Desktop/code/fruit_data_with_colors.txt","rb") as f:
    for block in iter(partial(f.read,64),b''):
        print(block)
print(locals())
print(globals())