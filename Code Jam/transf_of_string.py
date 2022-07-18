def transfor_str(S,F):    
    test_str=list(S)
    number_of_operation=0
    for i in range(len(test_str)):
        if ord(test_str[i])>ord(F):
            # print("larger",ord(test_str[i]),"======>",ord(F))
            difference=ord(test_str[i])-ord(F)
            # print("diference====>",difference)
            if difference>13:
                
                number_of_operation=number_of_operation+abs(difference-26)
            else:
                number_of_operation=number_of_operation+difference
            for j in range(difference):
                replace_str=ord(test_str[i])-1
                test_str[i]=chr(replace_str)
        if ord(test_str[i])<ord(F):
            # print("larger",ord(test_str[i]),"======>",ord(F))
            difference=abs(ord(test_str[i])-ord(F))
            # print("diference====>",difference)
            if difference>13:
                
                number_of_operation=number_of_operation+abs(difference-26)
            else:
                number_of_operation=number_of_operation+difference
            for j in range(difference):
                replace_str=ord(test_str[i])+1
                test_str[i]=chr(replace_str)
            
    # print(test_str)
    print("Case",number_of_operation)
def main():
    input_str=input("enter the string\n")
    replace_str=input("enter the char with replace\n\n")
    if len(replace_str)>1:
        print("enter one charcter")
        return 
    try:
        transfor_str(input_str,replace_str)
    except:
        print("error")


if __name__=="__main__":
    main()