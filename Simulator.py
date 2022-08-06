#Open text file, save lines to memory
f = open("C:/Users/mercu/OneDrive/Desktop/College/sem2/CO/Run.txt", 'r')
MEM = f.readlines()
f.close()

#initialise program counter
PC = 0
def pcPrinter (PC, base):
    '''returns binary value of program counter'''
    '''also can do binary conversion w extra zero bits appended for a given base length'''
    return((base-len(binVal))*'0' + binVal)
def binToDec(n):
    return int(n, 2)


#initialise register file
RF = {}
for i in range(8):
    RF[pcPrinter(i, 3)] = '0'*16

def keyReturn(d, s):
    '''Returns key which contains a given string'''
    for i in d.keys():
        if s in d[i]:
            return i


def executionEngine(instruction):
    types = {'A':['10000', '10001', '10110', '11010', '11011', '11100'], 'B':['10010', '11000', '11001'], 'C':['10011', '10111', '11101', '11110'], 'D':['10100', '10101'], 'E':['11111', '01100', '01101', '01111'], 'F':['01010']}
    opcode = instruction[:5]
    curType = keyReturn(types, opcode)

    if curType == 'A':
        r1 = instruction[7:10]
        r2 = instruction[10:13]
        r3 = instruction[13:]

        if opcode == '10000':
            #addition
            summ = binToDec(RF[r1]) + binToDec(RF[r2])
            if len(pcPrinter(summ, 0))>16:
                #overflow
                temp = list(RF['111'])
                temp[12] = 1
                RF['111'] = ''.join(temp)
            else:
                RF[r3] = pcPrinter(summ, 16)
        
        if opcode == '10001':
            #subtraction
            summ = binToDec(RF[r1]) - binToDec(RF[r2])
            if summ<0:
                #overflow
                temp = list(RF['111'])
                temp[12] = 1
                RF['111'] = ''.join(temp)
            else:
                RF[r3] = pcPrinter(0, 16)

        if opcode == '10110':
            #multiplication
            summ = binToDec(RF[r1])*binToDec(RF[r2])
            if len(pcPrinter(summ, 0))>16:
                #overflow
                temp = list(RF['111'])
                temp[12] = 1
                RF['111'] = ''.join(temp)
            else:
                RF[r3] = pcPrinter(summ, 16)
        
        if opcode == '11010':
            #bitwise xor
            RF[r3] = binToDec(RF[r1])^binToDec(RF[r2])
        
        if opcode == '11011':
            #bitwise or
            RF[r3] = binToDec(RF[r1])|binToDec(RF[r2])
        
        if opcode == '11100':
            #bitwise and
            RF[r3] = binToDec(RF[r1])&binToDec(RF[r2])

    if curType == 'B':
        r1 = instruction[5:8]
        imm = instruction[8:]

        if opcode == '10010':
            #mov immediate
            

    
    if curType == 'C':
        r1 = instruction[10:13]
        r2 = instruction[13:]
    
    if curType == 'D':
        r1 = instruction[5:8]
        memAddr = instruction[8:]
    
    if curType == 'E':
        memAddr = instruction[8:]
    
    # if curType == 'F':
