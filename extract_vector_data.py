#!/usr/bin/python
#script to find the -ve clock references in init section of the supplied vector file for DAQclk and DAQdata
#Adam Davis, STFC, 27/04/2018

#imports required
import sys
import pickle, pprint


# extract command line parmeters
if len(sys.argv) == 1:
    vector_file_name   = "QEM_D1_1111_Init_Loop_2.txt"
elif len(sys.argv) == 2:
    vector_file_name   = sys.argv[1]
else:
    print "use: analyse_vector_file.p <filename>"
    exit(0)

#print the file used
print "%s %s\n" % ("Vector file: ",vector_file_name)

#extract lines into array
with open(vector_file_name, 'r') as f:
    data = f.readlines()

    init_length  = int(data[0])
    loop_length  = int(data[1])
    signal_names = data[2].split()

#close file
f.close()

#define an empty array for clock references
clk_ref = []
latch = '1'

#find how many -ve clock edges and create a list of references
for i in range(init_length):
  line = data[i+3].split()
  format_line = "%64s" % line[0]
  y = format_line[63-22] #this this is 41 (dacCLKin) or 22 depending on what end is 0
  if y == '0':
     if latch == '0':
	 clk_ref.append(i+3)
         latch = '1'
  
  else :
     latch = '0'

#define an array base on number of clocks / references
length = len(clk_ref)
data_a = [0] * length

#extract data from -ve clock refereces
for i in range(length) :
  line = data[clk_ref[i]].split()
  format_line = "%64s" % line[0]
  y = format_line[63-20] #this this is 41 (dacCLKin) or 22 depending on what end is 0
  data_a[i]= y

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

#print the output to the screen
for i in range(19):
  print "%-20s%-10i %-5s%s%s%s%s%s%-4s %s%s%s%s%s%s" % (names[18-i] ,i+1, clk_ref[i],data_a[i*6 + 0] ,data_a[i*6 + 1],data_a[i*6 + 2] ,data_a[i*6 + 3] ,data_a[i*6 + 4] ,data_a[i*6 + 5] ,data_a[i*6 + 114] ,data_a[i*6 +115],data_a[i*6 + 116] ,data_a[i*6 + 117] ,data_a[i*6 + 118] ,data_a[i*6 + 119])

l=[]
i=0
while i < length:
	l.append([clk_ref[i], data_a[i]])
	i+=1
print(len(l))
#print(l)

t = open ("tmp2.pkl", 'wb')
pickle.dump(l, t)
t.close()

