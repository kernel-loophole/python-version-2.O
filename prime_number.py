from numpy import number


def prime_range(number1,number2):
    if number1==number2:
        return 0
    prime_number_list=[]
    for i in range(number1,number2):
        for j in range(2,i):
            if i%j==0:
                # print("prime",i,i%j)
                break
            else:
                if j+1==i:
                    
                    prime_number_list.append(i)
    return prime_number_list                    
                
def main():
    print(prime_range(10000000,10001000))
if __name__=="__main__":
    main()
    