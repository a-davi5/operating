#!/usr/bin/python
#script to find the -ve clock references in init section of the supplied vector file for DAQclk and DAQdata
#Adam Davis, STFC, 27/04/2018

#imports required
import sys
import numpy as np
import pickle, pprint
import time

# extract command line parmeters
if len(sys.argv) == 3:
    register_to_change = sys.argv[1]
    new_value = str(sys.argv[2])
    if len(new_value) != 6:
	print "2nd argument too long/short"
	print "use: analyse_vector_file.p <register to change (1-19)> <new value (6-bit string, eg 100011)>"
	exit(0)
    
    if int(register_to_change) < 1 | int(register_to_change) > 19 :
	print "1st argument out of range, to small"
	print "use: analyse_vector_file.p <register to change (1-19)> <new value (6-bit string, eg 100011)>"
	exit(0)
	
    if int(register_to_change) > 19 :
	print "1st argument out of range, to big (1-19)"
	print "use: analyse_vector_file.p <register to change (1-19)> <new value (6-bit string, eg 100011)>"
	exit(0)


else:
    print "use: analyse_vector_file.p <register to change (1-19)> <new value (6-bit string, eg 100011)>"
    exit(0)

#define a list of register names
names=["iBiasPLL",# 010100
"iBiasLVDS",# 101101
"iBiasAmpLVDS",# 010000
"iBiasADC2",# 010100
"iBiasADC1",# 010100
"iBiasCalF",#  010010
"iFbiasN",#  011000
"vBiasCasc",#  100000
"iCbiasP",#  011010
"iBiasRef",#  001010
"iBiasCalC",#  001100
"iBiasADCbuffer",#  001100
"iBiasLoad",#  010100
"iBiasOutSF",#  011001
"iBiasSF1",#  001010
"iBiasPGA",#  001100
"vBiasPGA",#  000000
"iBiasSF0",#  000101
"iBiasCol"]#  001100

# set filename
file_name   = "tmp2.pkl"

#print the file used
print "%s %s\n" % ("pkl file used: ",file_name)

# extract the data
pkl_file = open(file_name, 'rb')
new_data = pickle.load(pkl_file)

#close file
pkl_file.close()

print(new_data)


for i in range(19):
	print "%-20s%-10i %s%s%s%s%s%-4s %s%s%s%s%s%s" % (names[18-i] ,i+1 ,new_data[i*6 + 0][1] ,new_data[i*6 + 1][1],new_data[i*6 + 2][1] ,new_data[i*6 + 3][1] ,new_data[i*6 + 4][1] ,new_data[i*6 + 5][1] ,new_data[i*6 + 114][1] ,new_data[i*6 +115][1],new_data[i*6 + 116][1] ,new_data[i*6 + 117][1] ,new_data[i*6 + 118][1] ,new_data[i*6 + 119][1])


reg=int(register_to_change)
value = list(new_value)

l=[]

i = 0

while i < len(new_data):
	l.append([new_data[i][0], new_data[i][1]])
	i+=1


for i in range(6):
	l[((reg-1)*6)+i][1]=value[i]
	l[(((reg-1)+19)*6)+i][1]=value[i]


for i in range(19):
	print "%-20s%-10i %s%s%s%s%s%-4s %s%s%s%s%s%s" % (names[18-i] ,i+1 ,l[i*6 + 0][1] ,l[i*6 + 1][1],l[i*6 + 2][1] ,l[i*6 + 3][1] ,l[i*6 + 4][1] ,l[i*6 + 5][1] ,l[i*6 + 114][1] ,l[i*6 +115][1],l[i*6 + 116][1] ,l[i*6 + 117][1] ,l[i*6 + 118][1] ,l[i*6 + 119][1])


t = open ("tmp3.pkl", 'wb')
pickle.dump(l, t)
t.close()


