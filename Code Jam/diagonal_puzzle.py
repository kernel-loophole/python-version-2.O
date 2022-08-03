import numpy as np
def doc_str():
    doc_string='''The puzzle consists of an N by N grid of squares. Each square is either black or white. 
=======>The goal of the puzzle is to make all the squares black in as few moves as possible.
        In a single move, you may choose any diagonal of squares and flip the color of every square on that diagonal (black becomes white and white becomes black). For example, the 10 possible diagonals for a 3 by 3 grid are shown below.
example
            /..      ./.      ../      ...      ...
            ...      /..      ./.      ../      ...
            ...      ...      /..      ./.      ../
        --------------------------------------------->
            ...      ...      \..      .\.      ../
            ...      \..      .\.      ..\      ...
            \..      .\.      ..\      ...      ...
    Given the initial configuration of the board, what is the fewest moves needed to make all the squares black? 
    You are guaranteed that it is possible to make all the squares black.'''

    print(doc_string)
def make_data():
    values=np.array([['#','#','#'],['#','.','#'],['#','.','.']])
    return values

def main():
    array_1=make_data()
    diagonal_values=array_1.diagonal()
    diagonal_values_1=np.flipud(array_1).diagonal()
    diagonal_check=True
    
    for i in diagonal_values:
        for j in diagonal_values:
            if i==j:
                # print("con...")
                continue
            else:
                # print("not the same value")
                diagonal_check=False
                break
    # print(array_1)
    if diagonal_check:
        #change the vlaue s
        pass   
    for i in diagonal_values_1:
        for j in diagonal_values_1:
            if i==j:
                print("con...")
                continue
            else:
                # print("not the same value")
                diagonal_check=False
                break
    
    print(array_1)
    if not diagonal_check:
        for i in range(0,2):    
            sub_array=array_1[:2,:2]
            sub_array_1=array_1[1::,:2]
            sub_array_2=array_1[:2,1:3]
            sub_array_3=array_1[1:,:2]
            sub_array_4=array_1[1:,1:3]
            list_of_array=[sub_array,sub_array_1,sub_array_2,sub_array_3,sub_array_4]
            # print(sub_array)
            # print(sub_array_1)
            # print(sub_array_2)
            # print(sub_array_3)
            # print(sub_array_4)
            
            # for i in range(0,len(sub_array_1)-1):
            #     if sub_array[i+1,i+1]!=sub_array[i,i]:
            #         sub_array[i+1,i+1],sub_array[i,i]=sub_array[i,i],sub_array[i+1,i+1]    
            #     if sub_array_1[i+1,i+1]==sub_array[i,i]:
            #         sub_array_1[i+1,1+i],sub_array_1[i,i]=sub_array_1[i,i],sub_array_1[i+1,1+i]
            # print(array_1)
            # print(list_of_array)
            check_list_for_array=[]
            counter=0
            # print("before list ",list_of_array)
            for i in list_of_array:
                # print(i)
            
                x= np.fliplr(i).diagonal()
                y= np.flipud(i).diagonal()
                for h in range(0,len(i)-1):            
                    if i[h,h]!=i[h+1,h+1]:
                        # print("before =====>",i)
                        if i[h,h]=='.':
                            i[h,h]='#'
                            # print("after array",i)
                        if i[h+1,h+1]=='#':
                            # i[h+1,h+1]='.'
                            pass
                            # print("after array====>",i)
                        # print(i[h,h],i[h+1,h+1])
                    if i[h,h]==i[h+1,h+1] :
                        if i[h,h]=='.':
                            i[h,h]='#'
                            i[h+1,h+1]='#'
                        counter+=1
                        check_list_for_array.append(counter)
            # print(check_list_for_array)
            # print("========> After")
            # print(list_of_array)
                    
                # print(x,y)
                # if x[0]!=x[1]:
                #    print(x)
                # if y[0]!=y[1]:
                #    print(y)
            # print(array_1)
            array_1[:2,:2]=list_of_array[1]
            array_1[1::,:2]=list_of_array[2]
            array_1[:2,1:3]=list_of_array[3]
            array_1[1:,:2]=list_of_array[4]
            print("==========")
            print(array_1)
        else:
            print("same values for diagonal")

if __name__=="__main__":
    main()
    