def subarray_sorting(array):
    
    if len(array)==0:
        print("empty")
        return
    counter=1
    store_set=[]
    for i in range(len(array)):
        check_list=[]
        for j in range(i+1,len(array)):
            print(array[j])
            if array[i]<array[j]:
                check_list.append(array[i])
                print(array[i])
                print("breaking")
                break
            else:
                check_list.append(array[i])
                store_set.append(check_list)
                counter+=1
            
                print("exiting")
                break
    print('no. of subarray\n',counter)
    # print(store_set)
def swapping(array):
    tmp_array=array
    if subarray_sorting(array)==1:
        return array
    for i in range(0,len(tmp_array)):
        for j in range(i+1,len(tmp_array)):
            if tmp_array[i]>tmp_array[j]:
                tmp_array[i],tmp_array[j]=tmp_array[j],tmp_array[i]
                print("swapping between",tmp_array[i],tmp_array[j])
    print(tmp_array)
    # print(subarray_sorting(tmp_array))
        


def main():
    array=[1,4,2,3]
    swapping(array)
    
if __name__=="__main__":
    main()