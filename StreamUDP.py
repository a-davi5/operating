#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 16:53:18 2018

@author: rha73
"""

import socket
import struct
import time
import numpy as np

class StreamUDP(object):

    def __init__(self, MasterTxUDPIPAddress='192.168.0.1', MasterTxUDPIPPort=65535, MasterRxUDPIPAddress='192.168.0.1', MasterRxUDPIPPort=65536,TargetTxUDPIPAddress='192.168.0.2', TargetTxUDPIPPort=65535, TargetRxUDPIPAddress='192.168.0.2', TargetRxUDPIPPort=65536, RxUDPBuf = 1024, UDPMTU=9000, UDPTimeout=10):

        self.txsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rxsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.rxsocket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, RxUDPBuf)

        self.rxsocket.bind((MasterRxUDPIPAddress, MasterRxUDPIPPort))
        self.txsocket.bind((MasterTxUDPIPAddress, MasterTxUDPIPPort))

        #self.rxsocket.settimeout(None)
        #self.txsocket.settimeout(None)

        self.rxsocket.setblocking(1)
        #self.txsocket.setblocking(1)

        self.TgtRxUDPIPAddr = TargetRxUDPIPAddress
        self.TgtRxUDPIPPrt  = TargetRxUDPIPPort

        self.UDPMaxRx = UDPMTU

        self.debug = False

        self.ack = False

    def __del__(self):
        self.txsocket.close()
        self.rxsocket.close()
        
    def get_Image(self):
        pkt_num = 1
        while pkt_num <= 7:
            #receive packet up to 8K Bytes
            pkt = rxsocket.recv(9000)
            #extract trailer
            pkt_len = len(pkt)
            if text_debug == 1:
                pkt_top = pkt_len - 8
                data0 = (ord(pkt[pkt_top+3]) << 24) + (ord(pkt[pkt_top+2]) << 16) + (ord(pkt[pkt_top+1]) << 8) + ord(pkt[pkt_top+0])
                data1 = (ord(pkt[pkt_top+7]) << 24) + (ord(pkt[pkt_top+6]) << 16) + (ord(pkt[pkt_top+5]) << 8) + ord(pkt[pkt_top+4])
                pkt_top = 8
                data2 = (ord(pkt[pkt_top+3]) << 24) + (ord(pkt[pkt_top+2]) << 16) + (ord(pkt[pkt_top+1]) << 8) + ord(pkt[pkt_top+0])
                data3 = (ord(pkt[pkt_top+7]) << 24) + (ord(pkt[pkt_top+6]) << 16) + (ord(pkt[pkt_top+5]) << 8) + ord(pkt[pkt_top+4])
                # print trailer
                pkt_str = "%08X  %08X %08X %08X %08X %08X" % (pkt_num, pkt_len, data0, data1, data2, data3)
                print pkt_str
            #build image
            pkt_1d_array=np.fromstring(pkt, dtype=np.uint8, count=pkt_len-8)
            pkt_2d_array = pkt_1d_array.reshape(32,256)
            insert_point = 32 * pkt_num
            sensor_image[insert_point:insert_point + 31,0:255] = pkt_2d_array[0:31,0:255]
            pkt_num = pkt_num + 1
        
        
        
        
        
        
        
        return