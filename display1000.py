#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 17:38:08 2018

@author: rha73
"""
import time
from QemCam import *
from qem_setter import QemSetter
import requests


####### this section for the QEM backplane interface

backplane=QemSetter(url="http://192.168.0.122")
####### end of backplane setup section





qemcamera = QemCam()

print qemcamera.server_ctrl_ip_addr

qemcamera.connect()

#increase ifg from minimum
qemcamera.set_ifg()

qemcamera.x10g_stream.check_trailer = True

qemcamera.set_clock()

qemcamera.turn_rdma_debug_0ff()

qemcamera.set_10g_mtu('data', 8000)
qemcamera.x10g_rdma.read(0x0000000C, '10G_0 MTU')

# N.B. for scrambled data 10, 11, 12, 13 bit raw=> column size 360, 396
qemcamera.set_10g_mtu('data', 7344)
qemcamera.set_image_size_2(102,288,11,16)

print qemcamera.x10g_stream.num_pkt

#set idelay in 1 of 32 80fs steps  - d1, d0, c1, c0
qemcamera.set_idelay(0,0,0,0)

time.sleep(1)

locked = qemcamera.get_idelay_lock_status()

# set sub cycle shift register delay in 1 of 8 data clock steps - d1, d0, c1, c0
# set shift register delay in 1 of 16 divide by 8 clock steps - d1, d0, c1, c0
#
# Shift 72 + 144 bits

qemcamera.set_scsr(7,7,7,7)		# sub-cycle (1 bit)
qemcamera.set_ivsr(0,0,27,27)		# cycle (8 bits)

#qemcamera.load_vectors_from_file('./QEM_D4_198_ADC_0.txt')

time.sleep(0.1)

qemcamera.get_aligner_status()

locked = qemcamera.get_idelay_lock_status()

print "%-32s %-8X" % ('-> idelay locked:', locked)

#print "%-32s" % ('-> Calibration started ...')




qemcamera.display_image_stream(1000)




#while(1):
#   n=100
#   i=0
#   aux = 11
#   print("stop me now, 5 seconds......")
#   time.sleep(5)
#   print("too late, restarted calibration\n")

#  while i < n:
	#move Aux reset
#	backplane.setResistorRegister('AUXSAMPLE',aux)
#	time.sleep(0.2)
	#Display and/or capture frames into a file
#	qemcamera.display_image_stream(50)
	#qemcamera.log_image_stream('/scratch/qem/adc_cal_AUXSAMPLE_%d' %aux, 1000)
#	i=i+1
#	aux = aux + 1
	#print("%d/100" %i)
	



time.sleep(1)

qemcamera.disconnect()

print "\n-> finished:"

