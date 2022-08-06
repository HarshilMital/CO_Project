import math
# taking space in memory and then converting it into bits 
Memory_Space=[x for x in input("Memory Space ").split(" ")]
s = [str(integer) for integer in Memory_Space[:-1]]
a_string = "".join(s) 
Mem_in_bits=int(a_string)
if Memory_Space[-2:]=='MB':
    Mem_in_bits=Mem_in_bits*2**23
elif Memory_Space[-2:]=='GB':
    Mem_in_bits=Mem_in_bits*2**33
elif Memory_Space[-2:]=='KB':
    Mem_in_bits=Mem_in_bits*2**13
elif Memory_Space[-2:]=='gB':
    Mem_in_bits=Mem_in_bits*2**30
elif Memory_Space[-2:]=='mB':
    Mem_in_bits=Mem_in_bits*2**20
elif Memory_Space[-2:]=='kB':
    Mem_in_bits=Mem_in_bits*2**10
else:
    Mem_in_bits=Mem_in_bits
Mem_in_bits=(math.log(Mem_in_bits,2))

#memory which is been adderessed (among the four options)
Mem_address_type1=input("Enter Bit/Nibble/Byte/Word ")
if Mem_address_type1=="Bit":
    Addressable_mem=2
    Mem_in_bits=Mem_in_bits/Addressable_mem
    Mem_address_type1=Mem_in_bits
elif Mem_address_type1=="Nibble":
    Addressable_mem=4
    Mem_in_bits=Mem_in_bits/Addressable_mem
    Mem_address_type1=Mem_in_bits
elif Mem_address_type1=="Byte":
    Addressable_mem=8
    Mem_in_bits=Mem_in_bits/Addressable_mem
    Mem_address_type1=Mem_in_bits



#FIRST TYPE OF QUESTIONS
Len_of_instruction=int(input("Length of Instruction "))
Len_of_register=int(input("Length of register "))

#minimum bit needed to represent an address in this will be
print("minimum bit needed to represent an address ",Mem_in_bits)

#no of bits in OPCode
OPCode=Len_of_instruction-(Len_of_register+Mem_in_bits)
print("Number of bits required by the OP Code ",OPCode)

#filler bits in Instruction
filler=Len_of_instruction-(OPCode+2*Len_of_register)
print("filler bits in Instruction bits ",filler)

#maximun no of instructions that can be supported by ISA
print("maximun no of instructions ",2**OPCode)

#maximun no of registers that can be supported by ISA
print("maximun no of registers ",2**Len_of_register)


#SECOND TYPE OF QUESTIONS
#Type 1
CPU_bits=int(input("Total number of bits for CPU "))
Mem_in_bits=(math.log(Mem_in_bits,2))
Mem_address_type2=input("Enter Bit/Nibble/Byte/Word ")
if Mem_address_type1=="Bit":
    Addressable_mem=2
    Mem_in_bits=Mem_in_bits/Addressable_mem
elif Mem_address_type2=="Nibble":
    Addressable_mem=4
    Mem_address_type2=Mem_in_bits/Addressable_mem
elif Mem_address_type2=="Byte":
    Addressable_mem=8
    Mem_address_type2=Mem_in_bits/Addressable_mem
elif Mem_address_type2=="Word":
    Mem_address_type2=Mem_in_bits/CPU_bits
print("Address Pin ",Mem_address_type1-Mem_address_type2)