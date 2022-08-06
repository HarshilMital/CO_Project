
#taking space in memory and then converting it into bits 
Memory_Space=[x for x in input().split()]
if Memory_Space[-1]=='B':
    Mem_in_bits=int(Memory_Space[:-2])*8*10**6
else:
    Mem_in_bits=int(Memory_Space[:-2])*10**6

#memory which is been adderessed (among the four options)
Mem_addressed=input()


#FIRST TYPE OF QUESTIONS
Len_of_instruction=int(input())
Len_of_register=int(input())

#minimum bit needed to represent an address in this will be


#no of bits in OPCode
print("Number of bits required by the OP Code 5bits \n")

#filler bits in Instruction
print("filler bits in Instruction 13 bits \n")

#maximun no of instructions that can be supported by ISA
print("")

#maximun no of registers that can be supported by ISA



#SECOND TYPE OF QUESTIONS'
#Type 1
CPU_bits=int(input("Total number of bits for CPU "))







