def find_same_lines(file1, file2):
    """
    Finds the lines that are the same in two files.
    """
    with open(file1, 'r') as f1:
        lines1 = f1.readlines()
        with open(file2, 'r') as f2:
            
            lines2 = f2.readlines()
           
            for line in lines1:
                x=line[0:4]
              
                for line2 in lines2:
                    y=line2[0:4]
                    print(x,y)
                    if x==y:
                        print(line2)
                        
                
            same_lines = [line for line in lines1 if line in lines2]
            return same_lines
if __name__ == '__main__':
    file1 = 'result.txt'
    file2 = 'vivid.txt'
    same_lines = find_same_lines(file1, file2)
    print(same_lines)