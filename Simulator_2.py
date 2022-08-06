import sys
import matplotlib.pyplot as plt
import numpy as np
#Open text file, save lines to memory
# f = open("C:/Users/mercu/OneDrive/Desktop/College/sem2/CO/Run.txt", 'r')
instrSet = sys.stdin.readlines()
instrSet = [line.rstrip() for line in instrSet]
# f.close()


#initialise MEM
MEM = ['0'*16 for i in range(256)]
for i in range(len(instrSet)):
    MEM[i] = instrSet[i]


#initialise program counter
PC = 0
pcMod = False
def pcPrinter (PC, base):
    '''returns binary value of program counter'''
    '''also can do binary conversion w extra zero bits appended for a given base length'''
    binVal = bin(PC)[2:]
    return((base-len(binVal))*'0' + binVal)
def binToDec(n):
    return int(n, 2)

def floating_to_binary(n):
    if (n > 252) or (n < 1):
        return -1
    n = str(n)
    fltnum = n.split('.')
    exp = ''
    mantissa = ''
    fltlst = []
    fltlst.append(bin(int(fltnum[0]))[2:])
    fltlst.append(float('0.'+fltnum[1]))
    

    bnry_dcml_pt = ''
    cntr = 0
    k = fltlst[1]
    # print(k)
    while True:
        cntr += 1
        if str(k * 2)[0] == '1':
            bnry_dcml_pt += '1'
            k = k * 2 - 1
        else:
            bnry_dcml_pt += '0'
            k *= 2
        # print(k)
        if (k == 1) or (cntr > 7-len(fltlst[0])) or (k == 0):
            break
        
    # print(bnry_dcml_pt)
    # if (cntr > 7-len(fltlst[0])):
    #     print('error')
    # else:
    exp = bin(len(fltlst[0]) - 1)[2:]
    exp = ((3 - len(exp)) * '0') + exp
    # print(exp)
    mantissa = fltlst[0][1:] + bnry_dcml_pt[::-1]
    # print(mantissa)
    mantissa = mantissa + ((5 - len(mantissa)) * '0')
    return ((exp + mantissa)[:8])

def binary_to_floating(n):
    exp_bin = n[:3]
    exp = int(exp_bin, 2)
    mantissa_bin = n[3:]
    left_dec_pt = int('1' + mantissa_bin[:exp] + '0' * (exp - len(mantissa_bin[:exp])), 2)
    right_dec_pt = 0
    if len(mantissa_bin[:exp]) != 0:
        for i in range(len(mantissa_bin[exp:])):
            right_dec_pt += int(mantissa_bin[i + exp]) / (2 ** (i + 1))
    
    final_float = float(left_dec_pt + right_dec_pt)
    return final_float

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
def resetFlags():
    '''resets Flags'''
    global RF
    RF['111'] = '0'*16

memY = []
def executionEngine(instruction):
    '''executes given instruction from MEM'''
    instruction = instruction.strip('\n')
    types = {'A':['00000','00001','10000', '10001', '10110', '11010', '11011', '11100'], 'B':['00010','10010', '11000', '11001'], 'C':['10011', '10111', '11101', '11110'], 'D':['10100', '10101'], 'E':['11111', '01100', '01101', '01111'], 'F':['01010']}
    opcode = instruction[:5]
    curType = keyReturn(types, opcode)
    reset = 1
    global PC
    global memAccess
    global pcMod
    memAccess = [PC]

    if curType == 'A':
        r1 = instruction[7:10]
        r2 = instruction[10:13]
        r3 = instruction[13:]

        if opcode == '00000':
            summ = binary_to_floating(RF[r1][8:]) + binary_to_floating(RF[r2][8:])
            if summ > 252:
                temp = list(RF['111'])
                temp[12] = '1'
                RF['111'] = ''.join(temp)
                reset = 0
                RF[r3] = RF[r3] % (2 ** 16)
            else:
                RF[r3] = '00000000' + floating_to_binary(summ)

        if opcode == '10000':
            #addition
            summ = binToDec(RF[r1][8:]) + binToDec(RF[r2][8:])
            if len(pcPrinter(summ, 0))>16:
                #overflow
                temp = list(RF['111'])
                temp[12] = '1'
                RF['111'] = ''.join(temp)
                reset = 0
                RF[r3] = RF[r3] % (2 ** 16)
            else:
                RF[r3] = pcPrinter(summ, 16)
        
        if opcode == '10001':
            #subtraction
            summ = binToDec(RF[r1]) - binToDec(RF[r2])
            if summ<0:
                #overflow
                temp = list(RF['111'])
                temp[12] = '1'
                RF['111'] = ''.join(temp)
                reset = 0
                RF[r3] = pcPrinter(0, 16)
            else:
                RF[r3] = pcPrinter(summ, 16)

        if opcode == '00001':
            #subtraction
            summ = binary_to_floating(RF[r1]) - binary_to_floating(RF[r2])
            if summ<0:
                #overflow
                temp = list(RF['111'])
                temp[12] = '1'
                RF['111'] = ''.join(temp)
                reset = 0
                RF[r3] = pcPrinter(0, 16)
            else:
                RF[r3] = '00000000' + floating_to_binary(summ)

        if opcode == '10110':
            #multiplication
            summ = binToDec(RF[r1])*binToDec(RF[r2])
            if len(pcPrinter(summ, 0))>16:
                #overflow
                temp = list(RF['111'])
                temp[12] = '1'
                RF['111'] = ''.join(temp)
                reset = 0
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

        if opcode == '00010':
            #mov immediate
            RF[r1] = '0'*8 + imm

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
                temp[12] = '1'
                RF['111'] = ''.join(temp)
                reset = 0
            else:
                RF[r1] = pcPrinter(valee, 16)
        

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
                temp[13] = '1'
                RF['111'] = ''.join(temp)
                reset = 0
            elif binToDec(RF[r1]) > binToDec(RF[r2]):
                temp = list(RF['111'])
                temp[14] = '1'
                RF['111'] = ''.join(temp)
                reset = 0
            else:
                temp = list(RF['111'])
                temp[15] = '1'
                RF['111'] = ''.join(temp)
                reset = 0


    if curType == 'D':
        r1 = instruction[5:8]
        memAddr = instruction[8:]
        
        if opcode == '10100':
            #load
            RF[r1] = MEM[binToDec(memAddr)]
        
        if opcode == '10100':
            #store
            MEM[binToDec(memAddr)] = RF[r1]
        
        memAccess.append(binToDec(memAddr))
    

    if curType == 'E':
        memAddr = instruction[8:]
        global pcMod

        if opcode == '11111':
            #unconditional jump
            PC = binToDec(memAddr)
            pcMod = True
            memAccess.append(binToDec(memAddr))

        if opcode == '01100':
            #jump if less than
            if int(RF['111'][13]):
                PC = binToDec(memAddr)
                pcMod = True
                memAccess.append(binToDec(memAddr))

        if opcode == '01101':
            #jump if greater than
            if int(RF['111'][14]):
                PC = binToDec(memAddr)
                pcMod = True
                memAccess.append(binToDec(memAddr))
        
        if opcode == '01111':
            #jump if equal
            if int(RF['111'][15]):
                PC = binToDec(memAddr)
                pcMod = True
                memAccess.append(binToDec(memAddr))
    
    if curType == 'F':
        global halt
        halt = True

    if reset:
        resetFlags()


cycle = 0
cyclesX = []
while not halt:
    instruction = MEM[PC]
    executionEngine(instruction)
    

    print(pcPrinter(PC, 8), end = ' ')
    regList = []
    
    for i in range(8):
        regList.append(RF[pcPrinter(i, 3)])
    print(' '.join(regList))


    if pcMod:
        pcMod = False
    else: 
        PC +=1

    cycle +=1
    for i in range(len(memAccess)):
        #memAccess contains all the memory addresses accessed in decimal form
        #they're appended with the corresponding cycle to memY
        cyclesX.append(cycle)
        memY.append(memAccess[i])


for i in MEM:
    print(i.strip('\n'))


plt.scatter(cyclesX, memY, color='teal', marker='.')
plt.title('Memory Address vs Cycle Number', fontsize=14)
plt.xlabel('Cycle Number', fontsize=14)
plt.ylabel('Memory Address', fontsize=14)
plt.show()