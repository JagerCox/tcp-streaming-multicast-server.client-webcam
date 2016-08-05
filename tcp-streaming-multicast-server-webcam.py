#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import time
import json
import socket
import base64
import numpy as np
from threading import Thread

"""
    File name: tcp-streaming-multicast-server-webcam.py
    Author: Jäger Cox // jagercox@gmail.com
    Date created: 04/08/2016
    License: MIT
    Python Version: 2.7
    Revision: PEP8
"""

__author__ = "Jäger Cox // jagercox@gmail.com"
__created__ = "04/08/2016"
__license__ = "MIT"
__version__ = "0.1"
__python_version__ = "2.7"
__email__ = "jagercox@gmail.com"

SERVER_IP = "0.0.0.0"
SERVER_PORT = 953
MAX_NUM_CONNECTIONS = 20


class ConnectionPool(Thread):

    def __init__(self, ip, port, conn, device):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.conn = conn
        self.device = device
        print "[+] New server socket thread started for " + self.ip + ":" + \
            str(self.port)

    def run(self):
        try:
            while True:
                ret, frame = self.device.read()
                data = frame.tostring()
                self.conn.sendall(base64.b64encode(data) + '\r\n')
        except:
            print "Connection lost with " + self.ip + ":" + str(self.port)
        self.conn.close()

if __name__ == '__main__':
    camera = cv2.VideoCapture(0)
    print "Waiting connections..."
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection.bind((SERVER_IP, SERVER_PORT))
    connection.listen(MAX_NUM_CONNECTIONS)
    while True:
        (conn, (ip, port)) = connection.accept()
        thread = ConnectionPool(ip, port, conn, camera)
        thread.start()
    connection.close()
    camera.release()
