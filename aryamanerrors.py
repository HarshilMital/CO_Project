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


    #i