import random
from stringcolor import *
def binary_str_game(binary_str):
    if len(binary_str)==0:
        print("please provide valid binary string")
        return
    if len(binary_str)%2 !=0:
        return 
    binary_string=list()
    Alice=0
    Bob=0
    alice_bob_check=True
    # print(binary_string)
    for i in range(0,int(len(binary_str))):
        # print(binary_str[i])
        binary_string.append(binary_str[i])
    print(binary_string)
    while True:
        if len(binary_string)<=2:
            if binary_string[0]==0 and binary_string[1]==1:
                print("done")
            if binary_string[0]==0 and binary_string[1]==1:
                print("done")
                
            else:
                print(cs('no move remain',"red"))
                break
            
        
        x=random.choice(binary_string)
        y=random.choice(binary_string)
     
        if x=='0' and y=='1':
            print("removing",x,y)
            binary_string.remove(y)
            binary_string.remove(x)
            if alice_bob_check:
                Alice+=1
                alice_bob_check=False
            else:
                Bob+=1
                alice_bob_check=True
        if y=='0' and x=='1':
            print("removing",x,y)
            binary_string.remove(y)
            binary_string.remove(x)
            if alice_bob_check:
                Alice+=1
                alice_bob_check=False
            else:
                Bob+=1
                alice_bob_check=True
    print(binary_string)
    print("alice move",Alice)
    print(cs('bob move',"yellow"),Bob)
    if Alice>Bob:
        return True
    else:
        return False

if __name__=="__main__":
    if binary_str_game("01010010"):
        print("Alice wins")
    else:
        print("bob wins")