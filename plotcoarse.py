#!/usr/bin/env python2
import time
import h5py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import glob, os

#function to extract the coarse bits for a column for a single adc (33)
def getcoarsebitscolumn(input):
    new_list = []
    for i in input:
        for j in i:
		new_list.append((j[33]&1984)>>1) # extract the coarse bits
    return new_list

# generate a list of h5 files
def Listh5Files():
    filenames=[]
    #os.chdir("/mydir")
    for file in glob.glob("/scratch/qem/coarse/*.h5"):
        filenames.append(file)
        #print(file)
    filenames.sort()
    return filenames

#Generate the coarse voltages
def generatecoarsevoltages(length):
	voltages=[]
	for i in range(length):
		voltages.append(float(0.3428 + (i * 0.00153)))
	return voltages


###### MAIN ######
#array for files that need processing
filelist=[]
#array of voltages for the plot
voltages = []
#array of column averages for the plot
averages = []
#generate a list of files to process
filelist=Listh5Files()
#populate the voltage array
voltages = generatecoarsevoltages(len(filelist))


#process the files in filelist
for i in filelist:
	f=h5py.File(i, 'r')
	print(i)
	a_group_key = list(f.keys())[0]
	data = list(f[a_group_key])
	column=getcoarsebitscolumn(data)
	#average the data
	average = sum(column) / len(column)
	averages.append(average)
	f.close()

#generate and plot the graph
plt.plot(voltages, averages, '-')
plt.grid(True)
plt.xlabel('Voltage')
plt.ylabel('coarse value')
plt.savefig("coarse.png", dpi = 100)
plt.show()

