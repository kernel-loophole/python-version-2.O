def check_match(string):
    check_list=["abc","xyz","none","etc"]
    for i in check_list:
        match string:
            case 'abc':
                print("string is abc")
            case 'xyz':
                print("string is xyz")
            case _:
                print("string is not abc and xyz")
    return
if __name__=="__main__":
    check_match(input())
