#a g h gensyntax

def errors2():
    global lines
    global errorList
    hlt_flag = False


    for i in range(len(lines)):

            #g
            #just checks if var statement is present outside the inital block of var declaration
            if (lines[i][0] == 'var') and (i > var_count):
                if errorList[i] == None:
                    errorList[i] == 'g'

            #h
            if (lines[i][0] == 'hlt'):
                hlt_flag = True

            if (i == len(lines) - 1) and not (hlt_flag):
                if errorList[i] == None:
                    errorList[i] == 'h'

            #i

            if (i == len(lines) - 1):
                if (lines[i][0] == 'hlt') or (lines[i][0][-1] ==':' and lines[i][1] == 'hlt'):
                    if errorList[i] == None:
                        errorList[i] == 'i'

            

            #general syntax error for the case of anything
            # check if all the words present in the keywords list or occurs after var or a label(not neccesarily valid)
            # or $integer 

            keywords = ['add', 'sub', 'ld', 'st', 'mul', 'div', 'rs', 'ls', 'xor', 'or', 'and', 'not', 'cmp', 'jmp', 'jlt', 'jgt', 'je', 'hlt', 'mov', 'var', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R0', 'FLAGS'] 

            for j in lines[i]:
                if (j not in keywords) and (j[-1] != ':') and (lines[i][lines[i].index(j) - 1] != 'var') and (j[0] != '$'):
                    if errorList[i] == None:
                        errorList[i] == 'gse'

            



