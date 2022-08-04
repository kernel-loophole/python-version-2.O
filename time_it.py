import timeit

def test():
    for i in range(0,10):
        print(i)
     
if __name__=="__main__":
    print(timeit.timeit('test()',setup="from __main__ import test"))

