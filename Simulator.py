#Open text file, save lines to memory
f = open("C:/Users/mercu/OneDrive/Desktop/College/sem2/CO/Run.txt", 'r')
MEM = f.readlines()
f.close()

#initialise program counter
PC = 0
def pcPrinter (PC, base):
    '''returns binary value of program counter'''
    '''also can do binary conversion w extra zero bits appended for a given base length'''
    binVal = bin(int(PC))[2:]
    return((base-len(binVal))*'0' + binVal)

#initialise register file
RF = {}
for i in range(8):
    RF[pcPrinter(i, 3)] = '0'*16




