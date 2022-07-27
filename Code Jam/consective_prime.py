from numpy import number
def prime_range(number1,number2,Z):
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
    consective_prime=[]
    for i in range(0,len(prime_number_list[::])-1):
        try:
            if prime_number_list[i]*prime_number_list[i+1]==Z or prime_number_list[i]*prime_number_list[i+1]<Z :
                
                consective_prime.append(prime_number_list[i]*prime_number_list[i+1])
        except:
            print("error")
    
    for i in range(1,len(consective_prime)-1):
        try:
            if consective_prime[i]<Z:
                consective_prime.remove(consective_prime[i]) 
        except:
            pass
    return max(consective_prime)
def main():
    ####### for range########
    # x=int(input("enter x range"))
    # y=int(input("enter y range "))
    
    #for consective prime number#
    x=1
    
    z=2022
    y=int(z/2)
    print(prime_range(x,y,z))
if __name__=="__main__":
    main()
    