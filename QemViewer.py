#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 13:22:54 2018

@author: rha73
"""
import sys
import numpy as np

import time
import numpy as np
import cv2
import h5py

import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

plt.subplot(3, 1, 3)

plt.ylabel('frequency')
plt.xlabel('ADC Value')
plt.title('Histogram of ADC Value')
#plt.axis([0, 255, 0, 65536])
plt.grid(True)
plt.show()




h5f = h5py.File('/data/qem1/test4.h5','r')
#h5f = h5py.File('/u/rha73/test4.h5','r')
image_set = h5f['dataset_1'][:]

num_images = len(image_set)

print num_images, np.min(image_set), np.average(image_set), np.max(image_set)

for i in range(1,num_images):
    plt.subplot(2, 1, 1)
    plt.imshow(image_set[i] & 0x400, cmap = "gray")
    plt.subplot(2, 1, 2)
    hi = image_set[i].reshape(102*288)
    plt.hist(hi[i], bins=16)
    plt.show()
    #plt.pause(0.01)
    print i, np.min(image_set[i]), np.average(image_set[i]), np.max(image_set[i]) & 0x400
    

h5f.close()
