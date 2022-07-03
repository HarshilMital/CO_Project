import CO_Assignment
import aryamanerrors.py
import harshilerrors.py
import ieshaanerrors.py


inp_file = open('Run.txt', 'r')
lines = inp_file.readlines()
for i in range(len(lines)):
    i.rstrip('\n')

lines = [i.split() for i in lines]
errorList = [None for i in range(256)]
