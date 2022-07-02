#a g h


inp_file = open('Run.txt', 'r')
lines = inp_file.readlines()
for i in range(len(lines)):
    i.rstrip('\n')

lines = [i.split() for i in lines]


errorList = [None for i in range(256)]

hlt_flag = False


for i in range(len(lines)):
    #  # checking for typos in instructions (other than lables)
    # if lines[i][0] not in ['add', 'sub', 'ld', 'st', 'mul', 'div', 'rs', 'ls', 'xor', 'or', 'and', 'not', 'cmp', 'jmp', 'jlt', 'jgt', 'je', 'hlt', 'mov', 'var']:
    #     if lines[i][0][:-1] not in labels:
    #         if errorList[i] == None:
    #             errorList[i] == 'a'
    # # checking for typos in registers
    # else:
    #     # also gonna have to account for presence of label and var 
    #     type = typeFinder(lines[i], opcodes)
    #     if (type == 'A'):
    #         if (lines[i][1] not in regAddress) or (lines[i][2] not in regAddress) or (lines[i][3] not in regAddress):
    #             if errorList[i] == None:
    #                 errorList[i] == 'a'

    #     elif (type == 'B'):
    #         memory[i] = (opcodes[inp[i][0]] + registerHandler(inp[i][1]) + immediateHandler(inp[i][2]))

    #     elif(type == 'C'):
    #         memory[i] = (opcodes[inp[i][0]] + '00000' + registerHandler(inp[i][1]) + registerHandler(inp[i][2]))

    #     elif (type == 'D'):
    #         memory[i] = (opcodes[inp[i][0]] + registerHandler(inp[i][1]) + memaddr_handler(inp[i][2]))
            
    #     elif (type == 'E'):
    #         memory[i] = (opcodes[inp[i][0]] + '000' + memaddr_handler(inp[i][1]))

    #     elif (type == 'F'):
    #         memory[i] = (opcodes[inp[i][0]]+'00000000000')

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
            if (lines[i][0] == 'hlt') or (lines[i][0][:-1] in labels and lines[i][1] == 'hlt'):
                if errorList[i] == None:
                    errorList[i] == 'i'

        



