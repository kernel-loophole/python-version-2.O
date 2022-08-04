def spilt_number(number):
    list_of_number=list(number)
    return list_of_number
def append_in_list(list):
    final_list_with_number=[]
    for i in range(0,len(list)):
        for j in range(0,int(list[i])):
            final_list_with_number.append(i+1)
    return final_list_with_number
def main_script(list__of_number):
    for j in range(0,len(list__of_number)):
        if j%2!=0:        
            list__of_number[j]=int(list__of_number[j])*-1
        else:
            list__of_number[j]=int(list__of_number[j])
    real_number=sum(list__of_number)        
    if real_number%11==0:
        print("divide")
    else:
        max_counter=0
        while max_counter<10:
            for l in range(0,len(list__of_number)):
                try:
                    list__of_number=swap_index(list__of_number,l,l+1)
                    print(list__of_number)
                    # for j in range(0,len(list__of_number)):
                    #     if j%2!=0  and list__of_number:
                    #         print("not ")        
                    #         list__of_number[j]=int(list__of_number[j])*1
                    #     else:
                    #         list__of_number[j]=int(list__of_number[j])*-1
                            
                    if sum(list__of_number)%11==0:
                        print("divide")
                        return list__of_number                        
                except:
                    # print("arror")
                    pass
            max_counter+=1
    print("no")
def swap_index(list__of_number,index_1,index_2):
    if list__of_number[index_1]>0 or list__of_number[index_2]<0:
        list__of_number[index_1]=list__of_number[index_1]*-1
        list__of_number[index_2]=abs(list__of_number[index_2])
    if list__of_number[index_1]<0 or list__of_number[index_2]>0:
        list__of_number[index_2]=list__of_number[index_2]*-1
        list__of_number[index_1]=abs(list__of_number[index_1])
    list__of_number[index_1],list__of_number[index_2]=list__of_number[index_2],list__of_number[index_1]
    return list__of_number

def main():
    list_1=spilt_number("002001039")
    print(main_script(append_in_list(list_1)))
if __name__=="__main__":
    main()