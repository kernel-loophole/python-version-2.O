import numpy as np
#recusrive algoritm for finding maximum number of coins 
def coin_test(matrix,len_of_matrix,sum_list,counter,sum,check_l):
    if len(matrix)==0:
        return 0
    if counter==len_of_matrix:
        sum_list.append(sum)
        sum=0
        check_l+=1
        counter=0
    make_check=0
    while True :
        try:
            sum_list.append(matrix[counter][make_check]+matrix[counter+1][make_check+1])
        except:
            pass
        if make_check==len_of_matrix:
            break
        make_check=make_check+1            
    if len_of_matrix+1==check_l:
        return sum_list
    try:
        sum_1=0
        sum_1=matrix[counter][counter]
        
        # print(sum_1)
    except:
        pass
    return coin_test(matrix,len_of_matrix,sum_list,counter+1,sum+sum_1,check_l)
def main():
    matrix=np.array([[0 ,0 ,0, 0 ,0],[1 ,1 ,1, 1 ,0],[2,2 ,2, 8 ,0],[1 ,1 ,1, 0 ,0],[0 ,0 ,0, 0 ,0]])
    matrix_1=np.array([[6,5,9],[8,54,20],[0,0,0]])
    sum_list=list()
    print(max(coin_test(matrix_1,len(matrix_1),sum_list, counter=0,sum=0,check_l=0)))

if __name__=="__main__":
    main()