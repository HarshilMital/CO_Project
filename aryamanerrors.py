import CO_Assignment
#a d e

def errors():
    inp_file = open('Run.txt', 'r')
    lines = inp_file.readlines()
    for i in range(len(lines)):
        i.rstrip('\n')

    lines = [i.split() for i in lines]
    errorList = [None for i in range(256)]

    
    #d
    #Illegal use of FLAGS register
    for i in range(len(lines)):
        if 'FLAGS' in lines[i]:
            curLine = lines[i]
            if (curLine[0][-1] == ':'):
                #if label is present at beginning of instruction
                curLine = curLine[1:]
            if curLine[0] != 'mov':
                if errorList[i] == None:
                    errorList[i] = 'd'

    #e
    #Illegal Immediate values (more than 8 bits)
    for i in range(len(lines)):
        if ((immediateHandler(lines[m])=='-1') or (immediateHandler(lines[m])=='-2')):
            if errorList[i] == None:
                    errorList[i] = 'e'

    #a
    #typos in instruction names or register names
    for i in range(len(lines)):
        type = typeFinder(lines[i], opcodes)
        if (type == '-1'):
            if errorList[i] == None:
                    errorList[i] = 'a'
            continue
        
        if (type == 'A'):
            if ((registerHandler(lines[i][1])== '-1') or (registerHandler(lines[i][2])=='-1')+ (registerHandler(lines[i][3])=='-1')):
                if errorList[i] == None:
                    errorList[i] = 'a'
            continue
        elif (type == 'B'):
            if ((registerHandler(lines[i][1])=='-1')):
                if errorList[i] == None:
                    errorList[i] = 'a'
            continue

        elif(type == 'C'):
            if ((registerHandler(lines[i][1])=='-1') or (registerHandler(lines[i][2])=='-1')):
                if errorList[i] == None:
                        errorList[i] = 'a'
            continue

        elif (type == 'D'):
            if ((registerHandler(lines[i][1])=='-1')):
                if errorList[i] == None:
                    errorList[i] = 'a'
            continue

        elif(type=='movB'):
            if ((registerHandler(lines[i][1])=='-1')):
                if errorList[i] == None:
                    errorList[i] = 'a'
            continue
        elif(type=='movC'):
            if ((registerHandler(lines[i][1])=='-1') or (registerHandler(lines[i][1])=='-1')):
                if errorList[i] == None:
                    errorList[i] = 'a'
            continue


    #Too many/few arguments + Incorrect arguments
    for i in range(len(lines)):
        type = typeFinder(lines[i], opcodes)
        length = len(lines[i])
        if (type == 'A'):
            if length != 4:
                if errorList[i] == None:
                    errorList[i] = 'gse'

        elif (type == 'B' or type=='movB'):
            if length != 3:
                if errorList[i] == None:
                    errorList[i] = 'gse'

        elif(type == 'C' or type=='movC'):
            if length != 3:
                if errorList[i] == None:
                    errorList[i] = 'gse'

        elif (type == 'D'):
            if length != 3:
                if errorList[i] == None:
                    errorList[i] = 'gse'
            
        elif (type == 'E'):
            if length != 2:
                if errorList[i] == None:
                    errorList[i] = 'gse'

        elif (type == 'F'):
            if length != 2:
                if errorList[i] == None:
                    errorList[i] = 'gse'
