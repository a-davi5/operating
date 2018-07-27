#!/usr/bin/python
#script to find the -ve clock references in init section of the supplied vector file for DAQclk and DAQdata
#Adam Davis, STFC, 27/04/2018

#imports required
import sys
import numpy as np
import pickle, pprint
import time
import h5py

# extract command line parmeters.  Usually use for ADC calibration so will use this as defualt
if len(sys.argv) == 1:
    print "use: analyse_vector_file.p <filename>"
    exit(0)
elif len(sys.argv) == 2:
    vector_file_name   = sys.argv[1]
else:
    print "use: analyse_vector_file.p <filename>"
    exit(0)

#extract lines into array
with open(vector_file_name, 'r') as f:
    data = f.readlines()
f.close()

length=len(data)

#extract the data from tmp3.pkl (new settings)
pkl_file = open('tmp3.pkl', 'rb')
new_data = pickle.load(pkl_file)

#close file
pkl_file.close()

#open a newfle with the orifional name appended with _mod.txt
f=open("%s_mod.txt" %vector_file_name, 'w')

#write the first three lines, don't change!!
f.write(data[0]) #
f.write(data[1])
f.write(data[2])
k=len(new_data) # assign k to the length of the new data array
j=0   		# number used to increment through the new_data array
m=0   		# number that increments by o after changing the lines
n=5  		# change number of lines before -ve clock edge
p=3  		# number of lines to change from to new value after the -ve clock edge
o=n+1+p  	# total number of lines to change from 'n' to new value, default is 1 extra + p

for i in range((length-3)-(k*(o-1))):
    if (j < k) : 			# if array increment value of new data is less than k (length of new data) do this, else just write the line to file
        if((i+m+n) == new_data[j][0]):  # looking forward by n, if the line number is equal to the first elemnt of array do this, else just write data to the file
            for l in range(o):	        # do this for the next 'o' number of lines
	        line = data[(i+m+l+3)]  # extract line from origional file
		f.write(line[0:43]) 	# write up to the reference point
		f.write(new_data[j][1]) # add new data from the file
		f.write(line[44:]) 	# add the rest of the origional line
	    j=j+1
            m=m+(o-1)
	else:	
            f.write(data[i+m+3])
    else:	
        f.write(data[i+m+3])
f.close()
print("\nNew file has been created, check folder")
