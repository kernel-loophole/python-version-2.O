from operator import xor
from random import randrange
import numpy as np
def equation(n,m):
    #intilize the array with 1's 
    
    list_numbers=np.arange(m)
    sub_array=np.array_split(list_numbers,n)
    counter=1
    max_=0
    value_of_k=0
    while counter<10 :
        for i  in range(0,len(sub_array)):           
            
            for j in sub_array[i]:
                stable_check=True
                multiple=list() 
                for k in range(0,len(sub_array)):
                    if stable_check:
                        multiple.append(j)
                        stable_check=False    
                        continue
                    try:
                        multiple.append(sub_array[k][counter])
                    except:
                        pass
                # if multiple[0]==0:
                #     print(multiple)       
                sum_=0
                for l in range(0,len(multiple)):
                    for q in range(0,int(m)):
                        print(q)
                        sum_=sum_+(int(multiple[l])^int(q))
                    
                        if max_<sum_ and sum_<m:
                            max_=sum_
                            value_of_k=q  
                            print("check if ===>",counter)   
        counter+=1    
                # print("sum=====>",sum_)
                # print("xor sum is ===>",xor_sum)
        counter=counter+1
    print("max_",max_)
    print("value of k",value_of_k*2)
if __name__=="__main__":
    equation(4,45)