#b c f
import CO_Assignment
def errors():
    inp_file = open('Run.txt', 'r')
    lines = inp_file.readlines()
    for i in range(len(lines)):
        i.rstrip('\n')

    lines = [i.split() for i in lines]
    errorList = [None for i in range(256)]

    #b
    def Error_handling_variables():
        for m in range(len(lines)):
            if (lines[m][0]=='var'): #for variables not present in the starting of the code
                if m+1>var_count:
                    if errorList[m]==None:
                            errorList[m]='g'
                    #print("variable not declared in the beg")
            if (lines[m][0][-1] == ":"):
                num = 1
            else:
                num = 0
            if ((lines[m][num] == 'ld') or (lines[m][num] == 'st')):
                if lines[m][num+1] not in variables:
                    #error = True
                    if lines[m][num+1] in labels:
                        if errorList[m]==None:
                            errorList[m]='f'
                    else:
                        if errorList[m]==None:
                            errorList[m]='b'
    #c
    def Error_handling_Labels():
        for m in range(len(inp)):
            if (inp[m][0][-1] == ":"):
                num = 1
            else:
                #incorrect usage of syntax
                num = 0
            if ((inp[m][num] == 'jmp') or (inp[m][num] == 'jlt') or (inp[m][num] == 'jgt') or (inp[m][num] == 'je')):
                if lines[m][num+1] not in labels:
                    #error = True
                    if lines[m][num+1] in variables:
                        if errorList[m]==None:
                            errorList[m]='f'
                    else:
                        if errorList[m]==None:
                            errorList[m]='a'
