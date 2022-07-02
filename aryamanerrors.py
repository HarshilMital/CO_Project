import CO_Assignment
#d e i

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
        if immediateHandler(lines[m])=='-1':
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
            
        #Necessary to process mov a movB and movC (instead of 'B' and 'C')
        #because mov has two different opcodes for movB and movC
        #so the opcodes dictionary doesn't contain mov at all, mov had to be done manually
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