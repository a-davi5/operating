#!/usr/bin/env python2
import time
import h5py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import glob, os


file_name="adc_cal_AUXSAMPLE_107.h5"
filelist=[]

def flatten3(input):
    new_list = []
    for i in input:
        for j in i:
	    for k in j:
		#l=k^63
		#m=(k&960)+l
                new_list.append((k&960)+(k&63)^63)
    return new_list

def getfinebitscolumn(input):
    new_list = []
    for i in input:
        for j in i:
		#o=(j[33])
		#k=(o&63)
		#l=k^63
		#m=((o&960)+l)
		#new_list.append(m)
		#new_list.append((j[33]&960)-(j[33]&63)) # subtract the last 6 bits from the coarse bits
		new_list.append((j[33]&1984)>>1) # extract the coarse bits
		#new_list.append(j[33])
		#new_list.append((j[33]&992)+(j[33]&31)^31) #this is the last 5 bits inverted
		#new_list.append((j[33]&960) + (j[33]&63)^63)
    return new_list

def flatten2(input):
    new_list = []
    for i in input:
        for j in i:
		#o=(j[33])
		#k=(o&63)
		#l=k^63
		#m=((o&960)+l)
		#new_list.append(m)
		new_list.append((j[33]&1984)-(j[33]&63)) # subtract the last 6 bits from the coarse bits
		#new_list.append(j[33])
		#new_list.append((j[33]&992)+(j[33]&31)^31) #this is the last 5 bits inverted
		#new_list.append((j[33]&960) + (j[33]&63)^63)
    return new_list

def Listh5Files():
    filenames=[]
    #os.chdir("/mydir")
    for file in glob.glob("/scratch/qem/coarse/*.h5"):
        filenames.append(file)
        #print(file)
    filenames.sort()
    return filenames

filelist=Listh5Files()

#print(filelist)
#print(len(filelist))

def generatefinevoltages(length):
	voltages=[]
	for i in range(length):
		voltages.append(float(1 + (i * 0.00008)))

	return voltages

def generatecoarsevoltages(length):
	voltages=[]
	for i in range(length):
		voltages.append(float(0.3428 + (i * 0.00153)))

	return voltages

voltages = []
voltages = generatecoarsevoltages(len(filelist))

averages = []
for i in filelist:
	#print(filelist[i])
	f=h5py.File(i, 'r')
	#print("Keys: %s" % f.keys())
	#f.close()
	print(i)
	a_group_key = list(f.keys())[0]
	data = list(f[a_group_key])
	#plt.clf()

	column=getfinebitscolumn(data)
	average = sum(column) / len(column)
	#print(average)
	averages.append(average)
	

	#for i in flat
	
	#plt.hist(flat, bins=5, align='mid', histtype='step')	
	#plt.hist(flat, bins=1000, range=[0,1000], align='mid', histtype='step')  # arguments are passed to np.histogram
	#plt.ylabel('counts')
	#plt.xlabel('ADC value')
	#plt.xaxis.set_major_locator(MaxNLocator(integer=true))
	#plt.grid(True)
	#plt.title(i)
	#plt.savefig("temp_%s.png" %i, dpi = 100)
	f.close()

#print(averages)
#print(voltages)

plt.plot(voltages, averages, '-')
plt.grid(True)
plt.xlabel('Voltage')
plt.ylabel('coarse value')
plt.savefig("coarse.png", dpi = 100)
plt.show()


"""

f=h5py.File(file_name, 'r')
print("Keys: %s" % f.keys())
for key in f.keys():
    print(key) #Names of the groups in HDF5 file.
a_group_key = list(f.keys())[0]

# Get the data
data = list(f[a_group_key])
flat=flatten3(data)
print(len(data))
plt.hist(flat, bins=99, range=[0,1000], align='mid', histtype='step')  # arguments are passed to np.histogram
plt.grid(True)
plt.title(file_name)
plt.savefig("%s.png" %file_name, dpi = 50)
plt.show()

"""
