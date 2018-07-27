#!/usr/bin/env python2
import time
from QemCam import *
from qem_setter import QemSetter
import requests

# Adam Davis

# extract command line parmeters
if len(sys.argv) == 1:
    frames = 1
    delay = 0
elif len(sys.argv) == 2:
    frames = int(sys.argv[1])
    delay = 0
elif len(sys.argv) == 3:
    frames = int(sys.argv[1])
    delay = int(sys.argv[2])
else:
    print "use: python adc_calibrate_coarse.py <No of frames> <delay (seconds)>"
    exit(0)


#### START Rob Halsall code ####
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
print "%-32s" % ('-> Calibration started ...')

#### END Rob Halsall code ####



#### START Adam Davis Code ####

####### this section for the QEM backplane interface
backplane=QemSetter(url="http://192.168.0.122")
####### end of backplane setup section

#define the number of loops for the adc calibration
n=1024
#define i and the staring point
i=0

#set the default starting point for the COARSE value
backplane.setResistorRegister('AUXSAMPLE_COARSE',435)

#main loop to capture the data
while i < n:
	#set the the AUXSAMPLE_FINE resistor to i
	backplane.setResistorRegister('AUXSAMPLE_FINE',i)

	#delay by 0 (default) or by the number passed to the function
	time.sleep(delay)
	#capture the data from the stream using rah function
	qemcamera.log_image_stream('/scratch/qem/fine/adc_cal_AUXSAMPLE_FINE_%04d' %i, frames)
	i=i+1
	#aux = aux + 1
	print("%d/1024" %i)
# end of main loop 

# wait for 1 second
time.sleep(1)

#disconnect from the camera
qemcamera.disconnect()

print "calibration data collected"

