'''
---GENERAL NOTES---
*ERRORS*
- Error case: last statement is a label instead of halt. KEEP IN MIND: THE LABEL CAN POINT TO HALT, I.E. LABEL1: HLT IS VALID
- General Syntaxt Error Case: More arguments entered than taken by the said instruction type
- General Syntaxt Error Case: Incorrect arguments for certain type of instruction
- input immediate is out of range (read immediate handler)

*OPTIMIZATIONS*
- Currently, this code, when it encounters a label which isn't inline w the following instruction, pops it, inserts it before the next line, and then stores its corresponding memory address 
    -> This could be optimized by simply popping the label out from the very beginning, and just storing its memory address.
    ++ Since this would allow the remainder of the code to skip a lot of arbitrary checks
'''

#Dictionary of all Instructions + OpCodes, sans move
opcodes =  {'add':'10000', 'sub':'10001', 'ld':'10100', 'st':'10101', 'mul':'10110', 'div':'10111', 'rs':'11000', 'ls':'11001', 'xor':'11010', 'or':'11011', 'and':'11100', 'not':'11101', 'cmp':'11110', 'jmp':'11111', 'jlt':'01100', 'jgt':'01101', 'je':'01111', 'hlt':'01010'}
types = {'A':['add', 'sub', 'mul', 'xor', 'or', 'and'], 'B':['rs', 'ls'], 'C':['div', 'not', 'cmp'], 'D':['ld','st'], 'E':['jmp', 'jlt', 'jgt', 'je'], 'F':['hlt']}


#8 registers, r0 to r7 (r7 being FLAGS), each denoted by its index
#each register stores 2 bytes, i.e. 16 bits
registers = ['0000000000000000' for i in range(8)]
regAddress = {'reg0':'000',' reg1':'001', 'reg2':'010', 'reg3':'011', 'reg4':'100', 'reg5':'101', 'reg6':'110', 'FLAGS':'111'}


#512 byte memory, 256 address, two bytes each
memory = ['0000000000000000' for i in range(256)]


#decimal to binary converter
def binary(n):
    #takes string/integer n and converts it to binary string
    return bin(int(n))[2:]



#VERIFY THIS LATER: PATH FOR FILE TO BE OPENED + ITS EXTENSION
#Take file 'Run.txt' as input, turns text into a line-by-line list called inp using f.readlines()
f = open("Run.txt", 'r')
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
# also pops out the var lines from imp



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
    global error
    error = True

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

    imm = rawInstruction[-1][1:]
    global error

    #if $13.00 is not a valid immediate:
    #Error check for invalid immediate value
    if ('.' in imm) or (int(imm)<0):
        error = True
        return '-1'
    
    binVal = binary(imm)
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

    if proposedRegister in regAddress:
        return regAddress[proposedRegister]
    else:
        global error
        error = True
        return '-1'
        









    

    
    
    





    

    

    

    

            


        

