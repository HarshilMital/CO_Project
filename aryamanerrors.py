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
    for i in range(len(inp)):
        type = typeFinder(inp[i], opcodes)
        print(inp[i])
        if (type == 'A'):
            memory[i] = (opcodes[inp[i][0]] + '00' + registerHandler(inp[i][1]) + registerHandler(inp[i][2])+ registerHandler(inp[i][3]))

        elif (type == 'B'):
            memory[i] = (opcodes[inp[i][0]] + registerHandler(inp[i][1]) + immediateHandler(inp[i][2]))

        elif(type == 'C'):
            memory[i] = (opcodes[inp[i][0]] + '00000' + registerHandler(inp[i][1]) + registerHandler(inp[i][2]))

        elif (type == 'D'):
            memory[i] = (opcodes[inp[i][0]] + registerHandler(inp[i][1]) + memaddr_handler(inp[i][2]))
            
        elif (type == 'E'):
            memory[i] = (opcodes[inp[i][0]] + '000' + memaddr_handler(inp[i][1]))

        elif (type == 'F'):
            memory[i] = (opcodes[inp[i][0]]+'00000000000')
        #Necessary to process mov a movB and movC (instead of 'B' and 'C')
        #because mov has two different opcodes for movB and movC
        #so the opcodes dictionary doesn't contain mov at all, mov had to be done manually
        elif(type=='movB'):
            memory[i]  = ('10010' + registerHandler(inp[i][1]) + immediateHandler(inp[i][2]))
        elif(type=='movC'):
            memory[i] = ('1001100000' + registerHandler(inp[i][1]) + registerHandler(inp[i][2]))