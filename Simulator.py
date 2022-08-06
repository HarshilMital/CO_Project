#Open text file, save lines to memory
f = open("C:/Users/mercu/OneDrive/Desktop/College/sem2/CO/Run.txt", 'r')
MEM = f.readlines()
f.close()

#initialise program counter
PC = 0
def pcPrinter (PC, base):
    '''returns binary value of program counter'''
    '''also can do binary conversion w extra zero bits appended for a given base length'''
    binVal = bin(PC)[2:]
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

halt = False
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
            RF[r1] = '0'*8 + imm

        if opcode == '11000':
            #right shift
            RF[r1] = pcPrinter((binToDec(RF[r1]) >> binToDec(imm)), 16)
        
        if opcode == '11001':
            #left shift
            valee = pcPrinter((binToDec(RF[r1]) << binToDec(imm)), 0)
            if len(valee)>16:
                temp = list(RF['111'])
                temp[12] = 1
                RF['111'] = ''.join(temp)
        

    if curType == 'C':
        r1 = instruction[10:13]
        r2 = instruction[13:]
    
        if opcode == '10011':
            #mov register
            RF[r2] = RF[r1]
        
        if opcode == '10111':
            #divide
            r3 = r1
            r4 = r2            
            r3Val = binToDec(RF[r3])
            r4Val = binToDec(RF[r4])
            quot = r3Val//r4Val
            remVal = r3Val%r4Val
            RF['000'] = pcPrinter(quot, 16)
            RF['001'] = pcPrinter(remVal, 16)

        if opcode == '11101':
            #bitwise not
            RF[r2] = pcPrinter(~binToDec(RF[r1]), 16)

        if opcode == '11110':
            #compare
            if binToDec(RF[r1]) < binToDec(RF[r2]): 
                temp = list(RF['111'])
                temp[13] = 1
                RF['111'] = ''.join(temp)
            elif binToDec(RF[r1]) > binToDec(RF[r2]):
                temp = list(RF['111'])
                temp[14] = 1
                RF['111'] = ''.join(temp)
            else:
                temp = list(RF['111'])
                temp[15] = 1
                RF['111'] = ''.join(temp)


    if curType == 'D':
        r1 = instruction[5:8]
        memAddr = instruction[8:]
        
        if opcode == '10100':
            #load
            RF[r1] = MEM[binToDec(memAddr)]
        
        if opcode == '10100':
            #store
            MEM[binToDec(memAddr)] = RF[r1]
    

    if curType == 'E':
        memAddr = instruction[8:]

        if opcode == '01100':
            #jump if less than
            if RF['111'][13]:
                PC = binToDec(memAddr)
        
        if opcode == '01101':
            #jump if greater than
            if RF['111'][14]:
                PC = binToDec(memAddr)
        
        if opcode == '01111':
            #jump if equal
            if RF['111'][15]:
                PC = binToDec(memAddr)
    
    if curType == 'F':
        halt = True