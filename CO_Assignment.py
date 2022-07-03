#Dictionary of all Instructions + OpCodes, sans move
opcodes =  {'add':'10000', 'sub':'10001', 'ld':'10100', 'st':'10101', 'mul':'10110', 'div':'10111', 'rs':'11000', 'ls':'11001', 'xor':'11010', 'or':'11011', 'and':'11100', 'not':'11101', 'cmp':'11110', 'jmp':'11111', 'jlt':'01100', 'jgt':'01101', 'je':'01111', 'hlt':'01010'}
types = {'A':['add', 'sub', 'mul', 'xor', 'or', 'and'], 'B':['rs', 'ls'], 'C':['div', 'not', 'cmp'], 'D':['ld','st'], 'E':['jmp', 'jlt', 'jgt', 'je'], 'F':['hlt']}


#8 registers, r0 to r7 (r7 being FLAGS), each denoted by its index
#each register stores 2 bytes, i.e. 16 bits
registers = ['0000000000000000' for i in range(8)]
regAddress = {'R0':'000','R1':'001', 'R2':'010', 'R3':'011', 'R4':'100', 'R5':'101', 'R6':'110', 'FLAGS':'111'}


#512 byte memory, 256 address, two bytes each
memory = ['0000000000000000' for i in range(256)]


#decimal to binary converter
def binary(n):
    #takes string/integer n and converts it to binary string
    return bin(int(n))[2:]



#VERIFY THIS LATER: PATH FOR FILE TO BE OPENED + ITS EXTENSION
#Take file 'Run.txt' as input, turns text into a line-by-line list called inp using f.readlines()
#C:/Users/mercu/OneDrive/Desktop/College/sem2/CO/Run.txt
f = open("C:/Users/mercu/OneDrive/Desktop/College/sem2/CO/Run.txt", 'r')
inp = f.readlines()
f.close()


#split each string in inp into a list. Make inp a list of lists
inp = [i.split() for i in inp]




'''
if labels are entered in format:
    apple:
        (further instructions)
the following script will clean it up into:
    apple: (further instructions)
if possible.
Edge case: last statement is a label (instead of halt, which should raise an error later)
'''
# inp = [i.split() for i in ['move r1 r2', 'label1:', 'add r1 r2', 'label2:', 'sub r1 r2']]
# inp = [i.split() for i in ['var a', 'var b', 'var c', 'mov r1 r2','label1:', 'add r1 r2', 'label2: sub r3 r4']]


labelInds = []
for i in range(len(inp)):
    if ((len(inp[i])==1) and (inp[i][0][-1]==':')):
        #i.e. if inp[i] = ['labelName:']
        if (i!= len(inp)-1):
            labelInds.append(i)
            inp[i+1].insert(0, inp[i][0])
labelInds.reverse()
for i in labelInds:
    inp.pop(i)


#variable processing
# checking for var at the begining of inp instructions and storing memory addresses in dictionary
# also pops out the var lines from inp



var_count = 0
variables = {}
for i in range(len(inp)):
    if (inp[i][0] == 'var'):
        var_count += 1
    else:
        break

for i in range(var_count):
    variables[inp[i][1]] = len(inp) - var_count + i

for i in range(var_count):
    inp.pop(0)



#dictionary to store labels
labels = {}
#loop to add all labels along with their indices into the labels dictionary
for i in range(len(inp)):
    if (inp[i][0][-1]==':'):
        labels[inp[i][0][:-1]] = i
        inp[i].pop(0)
#NOTE: If the last line is label (instead of halt), this will leave an empty string at the last index of inp 
#(i.e. [['move', 'r1', 'r2'], ['add', 'r1', 'r2'], ['sub', 'r1', 'r2'], []])

# print(labels)
# print(variables)
# print(inp)



#Code for errors will be processed here
error = False
errorCode = '' #this code store the error code? But hey, upto you how you do it   

def labelChecker(rawInstruction):
    #takes a line of inp (in the form [..., 'instruction', 'r1'...]) and checks whether the line has a label at the beginning
    if (rawInstruction[0][-1]==':'):
        lbl  = 1
    else:
        lbl = 0
    return(lbl)


def typeFinder(rawInstruction, opcodes, lbl = None):
    #takes a line of inp (in the form [..., 'instruction', 'r1'...]) and returns the type of instruction (A, B, C, D, E, F, movB, movC)
    
    if lbl == None:
        lbl = labelChecker(rawInstruction)
    #lbl = 1: 0th item in rawInstruction is a label, which needs to be ignored; else lbl = 0
    instruction = rawInstruction[lbl]    

    #THIS CODE IS CURRENTLY CONFIGURED TO NOT BE CASE SENSITIVE
    instruction = instruction.lower()
    
    #Case: mov
    if instruction.lower() == 'mov':
        #if label is present in the line, the index of the relevant word to check the type of move statement increases by 1
        if lbl == 0:
            keyword = rawInstruction[2][0]
        else:
            keyword = rawInstruction[3][0]
        
        if (keyword=='$'):
            return 'movB'
        else:
            return 'movC'
    

    #i iterates over all the types, checks if the instruction is of type i, and if yes, returns i
    for i in 'A B C D E F'.split():
        if instruction in types[i]:
            return i
    
    #if by this point in this function, return hasn't been executed, it implies an error. If the error happened up 
    return '-1'

#COME BACK TO THIS FOR SIMULATOR
# def flagsHandler(semantic, newVal):
#     #is semantic the right word? Anyway, takes 'V', 'L', 'G', & 'E' as inputs
#     #sets corresponding bit in flags to newVal
#     global registers

#     if semantic.upper() == 'V':
#         #overflow bit
#         num = -1
#     elif semantic.upper() == 'L'
#         #


def immediateHandler(rawInstruction):
    #converts decimal immediate to binary, checks if it's 8 bits and positive, if not, returns '-1'
    #ASSUMES IMMEDIATE IS ASSOCIATED WITH CORRECT TYPE OF INSTRUCTION (WHICH IS B) AND NOT MISMATCHED

    if (rawInstruction[-1][0]!='$'):
        return '-2Dollar'

    imm = (rawInstruction[-1]).lstrip('$')
    global error

    #if $13.00 is not a valid immediate:
    #Error check for invalid immediate value
    if ('.' in imm) or (int(imm)<0):
        error = True
        return '-1'
    
    try:
        binVal = binary(imm)
    except:
        return '-2notNum'
    length = len(binVal)
    if (length>8):
        error = True
        return '-1'
    
    #convert binary value into 8 bits
    finalVal = '0'*(8-length)+binVal
    return finalVal

def registerHandler(proposedRegister):
    # Register handler takes a proposed register from the rawInstruction i.e. a string representing what should be a valid resistor
    # if it's a valid registor, returns corresponding address
    # else, returns '-1'

    # This could later be modified to check for if the register is appropriate for the function (i.e. if flags is being used legally)

        # Following will be useful later for full blown line-by-line assembly to binary assembler:
        #     if labelChecker(rawInstruction):
        #         rawInstruction = rawInstruction[1:]
        #     #removes label if it's there
            
        #     curType = typeFinder(rawInstruction, opcodes, 0)
        #     #called typeFinder with lbl = 0 for optimization purposes, since now it won't have to fruitlessly run labelChecker script

    if proposedRegister[0]=='$':
        return '-2dollaR'
    
    if proposedRegister in regAddress:
        return regAddress[proposedRegister]
    else:
        return '-1'

# takes label/variable/ and converts it to binary memory address

def memaddr_handler(proposedMem_addr):

    mem = proposedMem_addr

    if mem in labels:
        mem = binary(labels[mem])
        return '0'*(8 - len(mem)) + mem

    elif mem in variables:
        mem = binary(variables[mem])
        return '0'*(8 - len(mem)) + mem

    return mem

inp_file = open('C:/Users/mercu/OneDrive/Desktop/College/sem2/CO/Run.txt', 'r')
lines = inp_file.readlines()
inp_file.close()
for i in (lines):
    i.rstrip('\n')

lines = [i.split() for i in lines]
errorList = [None for i in range(256)]

def errors1():
    global lines
    global errorList

    #Too many/few arguments + Incorrect arguments
    for i in range(len(lines)):
        lbl = labelChecker(lines[i])
        type = typeFinder(lines[i], opcodes)
        length = len(lines[i]) - lbl
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
            if length != 1:

                if errorList[i] == None:
                    errorList[i] = 'gse'

    #a
    #typos in instruction names or register names
    for i in range(len(lines)):
        if errorList[i] == None:
            if lines[i][0] == 'var':
                continue
            type = typeFinder(lines[i], opcodes)
            if (type == '-1'):
                errorList[i] = 'a'
                continue
            lbl = labelChecker(lines[i])
            
            if (type == 'A'):
                if ((registerHandler(lines[i][lbl+1])== '-1') or (registerHandler(lines[i][lbl+2])=='-1')+ (registerHandler(lines[i][lbl+3])=='-1')):
                    errorList[i] = 'a'
                continue
            elif (type == 'B'):
                if ((registerHandler(lines[i][lbl+1])=='-1')):
                    errorList[i] = 'a'
                continue

            elif(type == 'C'):
                if ((registerHandler(lines[i][lbl+1])=='-1') or (registerHandler(lines[i][lbl+2])=='-1')):
                    errorList[i] = 'a'
                continue
            
            elif (type == 'D'):
                if ((registerHandler(lines[i][lbl+1])=='-1')):
                    errorList[i] = 'a'
                continue
            
            elif(type=='movB'):
                if ((registerHandler(lines[i][lbl+1])=='-1')):
                    errorList[i] = 'a'
                continue
            elif(type=='movC'):
                if ((registerHandler(lines[i][lbl+1])=='-1') or (registerHandler(lines[i][lbl+1])=='-1')):
                    errorList[i] = 'a'
                continue
            
    
    #d
    #Illegal use of FLAGS register
    for i in range(len(lines)):
        if errorList[i] == None:
            if 'FLAGS' in lines[i]:
                curLine = lines[i]
                if (curLine[0][-1] == ':'):
                    #if label is present at beginning of instruction
                    curLine = curLine[1:]
                if curLine[0] != 'mov':
                    errorList[i] = 'd'

    #e
    #Illegal Immediate values (more than 8 bits)
    for i in range(len(lines)):
        if errorList[i] == None:
            type = typeFinder(lines[i], opcodes)
            if (type == 'B'):
                if ((immediateHandler(lines[i])=='-1') or (immediateHandler(lines[i])=='-2')):
                    if errorList[i] == None:
                            errorList[i] = 'e'

def errors2():
    global lines
    global errorList
    hlt_flag = False


    for i in range(len(lines)):
        if errorList[i] == None:
            #g
            #just checks if var statement is present outside the inital block of var declaration
            if (lines[i][0] == 'var') and (i > var_count):
                errorList[i] == 'g'

            #h
            if (lines[i][0] == 'hlt'):
                hlt_flag = True

            if (i == len(lines) - 1) and not (hlt_flag):
                errorList[i] == 'h'

            #i

            if (i == len(lines) - 1):
                if (lines[i][0] == 'hlt') or (lines[i][0][-1] ==':' and lines[i][1] == 'hlt'):
                    errorList[i] == 'i'

            

            #general syntax error for the case of anything
            # check if all the words present in the keywords list or occurs after var or a label(not neccesarily valid)
            # or $integer 

            keywords = ['add', 'sub', 'ld', 'st', 'mul', 'div', 'rs', 'ls', 'xor', 'or', 'and', 'not', 'cmp', 'jmp', 'jlt', 'jgt', 'je', 'hlt', 'mov', 'var', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R0', 'FLAGS'] 

            for j in lines[i]:
                if (j not in keywords) and (j[-1] != ':') and (lines[i][lines[i].index(j) - 1] != 'var') and (j[0] != '$'):
                    errorList[i] == 'gse'

def errors3():

    global lines
    global errorList

    #b
    
    for m in range(len(lines)):
        if errorList[m] == None:
            if (lines[m][0]=='var'): #for variables not present in the starting of the code
                if m+1>var_count:
                    errorList[m]='g'
                    #print("variable not declared in the beg")
            num = labelChecker(lines[m])
            if ((lines[m][num] == 'ld') or (lines[m][num] == 'st')):
                if lines[m][num+2] not in variables:
                    #error = True
                    if lines[m][num+2] in labels:
                        errorList[m]='f'
                    else:
                        errorList[m]='b'
    #c

    for m in range(len(lines)):
        if errorList[m] == None:
            if (lines[m][0][-1] == ":"):
                num = 1
            else:
                #incorrect usage of syntax
                num = 0
            if ((lines[m][num] == 'jmp') or (lines[m][num] == 'jlt') or (lines[m][num] == 'jgt') or (lines[m][num] == 'je')):
                if lines[m][num+1] not in labels:
                    #error = True
                    if lines[m][num+1] in variables:
                        errorList[m]='f'
                    else:
                        errorList[m]='c'
        
        for m in range(len(lines)):
            if errorList[m]==None:
                if (lines[m][0][-1] == ":"):
                    num = 1
                    if ((lines[m][1][-1] == ':')):
                        errorList[m]='gse'

errors1()
errors2()
errors3()

for i in errorList:
    if i!=None:
        error = True

def errorPrint():
    for i in range(len(errorList)):
        if errorList[i]!=None:
            if errorList[i] == 'a':
                print(f"Error (line {i+1}): Typos in instruction name or register name")
            if errorList[i] == 'b':
                print(f"Error (line {i+1}): Use of undefined variables")
            if errorList[i] == 'c':
                print(f"Error (line {i+1}): Use of undefined labels")
            if errorList[i] == 'd':
                print(f"Error (line {i+1}): Illegal use of FLAGS register")
            if errorList[i] == 'e':
                print(f"Error (line {i+1}): Illegal Immediate values (more than 8 bits)")
            if errorList[i] == 'f':
                print(f"Error (line {i+1}): Misuse of labels as variables or vice-versa")
            if errorList[i] == 'g':
                print(f"Error (line {i+1}): Variables not declared at the beginning")
            if errorList[i] == 'h':
                print(f"Error (line {i+1}): Missing hlt instruction")
            if errorList[i] == 'i':
                print(f"Error (line {i+1}): hlt not being used as the last instruction")
            if errorList[i] == 'gse':
                print(f"Error (line {i+1}): General Syntax Error")

#converts assembly instructions in inp to binary and loads the binary converted instructions into the memory
def binary_instruction_memload():
    for i in range(len(inp)):
        type = typeFinder(inp[i], opcodes)
        if (type == 'A'):
            memory[i] = (opcodes[inp[i][0]] + '00' + registerHandler(inp[i][1]) + registerHandler(inp[i][2])+ registerHandler(inp[i][3]))

        elif (type == 'B'):
            memory[i] = (opcodes[inp[i][0]] + registerHandler(inp[i][1]) + immediateHandler(inp[i]))

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
            memory[i]  = ('10010' + registerHandler(inp[i][1]) + immediateHandler(inp[i]))
        elif(type=='movC'):
            memory[i] = ('1001100000' + registerHandler(inp[i][1]) + registerHandler(inp[i][2]))
        
if error:
    errorPrint()
else:
    binary_instruction_memload()
    [print(i) for i in memory]








    

    
    
    





    

    

    

    

            


        

