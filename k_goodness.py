#k_goodness string 
#    a string is K_goodness
#if s[i] !=s[len(s)-i+1]
from numpy import number

#Main Function for K-goodness string finding 
def K_good_string(string,score):
    if len(string)==0:
        return 
    k_good=string
    # print(len(k_good))
    counter_for_score=0
    #first part of code
    for i in range(1,len(k_good)):
        try:
            if k_good[i]!=k_good[len(k_good)-i+1]:
                
                counter_for_score=counter_for_score+1
                # print(k_good[i],k_good[len(k_good)-i+1])
        
        except:
            continue
    # print("this will run ")
    if score==int(counter_for_score/2):
        return 0
    else:
        #second part of code [[[[[[[[second part]]]]]]]]
        swapping_index_right=0
        swapping_index_left=1
        number_operation=0
        while swapping_index_left!=len(k_good)/2:
            number_operation+=1
            k_good[swapping_index_left],k_good[swapping_index_right]=k_good[swapping_index_right],k_good[swapping_index_left]
            for i in range(1,len(k_good)):
                try:
                    if k_good[i]!=k_good[len(k_good)-i+1]:
                
                        counter_for_score=counter_for_score+1
                        # print(k_good[i],k_good[len(k_good)-i+1])
        
                except:
                    continue
                
                # if score==int(counter_for_score/2):
                #     return int(counter_for_score/2)
            swapping_index_left+=1
            swapping_index_right+=1
        return number_operation
        # K_good_string(make_string_k_goodness(string,swapping_index_left,swapping_index_right),score)  
if __name__=="__main__":
    string=input("enter the string")
    k_good=[]
    for i in range(0,len(string)):
        k_good.append(string[i])
    print("case==>",K_good_string(k_good,4))