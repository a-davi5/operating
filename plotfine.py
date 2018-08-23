#!/usr/bin/env python2
import time
import h5py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import glob, os

#author Adam Davis

#function to extract the fine data bits from the H5 file (chosen column 33 in this case)
def getfinebitscolumn(input):
    fine_data = []
    for i in input:
        for j in i:
		fine_data.append((j[33]&63)) # extract the fine bits
    return fine_data

#function to list the h5 files in a specific directory
def Listh5Files():
    filenames=[]
    #list the files in this directory
    for file in glob.glob("/scratch/qem/fine/*.h5"):
        filenames.append(file)
    #sort files alphabetically
    filenames.sort()
    return filenames

#function to generate the voltages given a specific length
def generatevoltages(length):
	voltages=[]
	for i in range(length):
		voltages.append(float(1 + (i * 0.00008)))
	return voltages

######    MAIN    ######
#array of files to be processed
filelist=[]
filelist=Listh5Files()
# voltages for the plot
voltages = []
voltages = generatevoltages(len(filelist))
# averaged data for the plot 
averages = []

# extract the data from each file in the folder
for i in filelist:
	#open the file in the filelist array
	f=h5py.File(i, 'r')
	print(i)
	#extract the data key from the file
	a_group_key = list(f.keys())[0]
	#get the data
	data = list(f[a_group_key])
	#get data for column
	column=getfinebitscolumn(data)
	#average the column data
	average = sum(column) / len(column)
	#add the averaged data to the averages[] array
	averages.append(average)
	#close the file
	f.close()


#generate the x / y plot of the data collected
plt.plot(voltages, averages, '-')
plt.grid(True)
plt.xlabel('Voltage')
plt.ylabel('fine value')
plt.savefig("fine.png", dpi = 100)
plt.show()


