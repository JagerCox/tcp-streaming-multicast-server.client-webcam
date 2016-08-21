#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import socket
import base64
import numpy as np

"""
    File name: tcp-streaming-multicast-client-webcam.py
    Author: Jäger Cox // jagercox@gmail.com
    Date created: 04/08/2016
    License: MIT
    Python Version: 2.7
    Code guide line: PEP8
"""

__author__ = "Jäger Cox // jagercox@gmail.com"
__created__ = "04/08/2016"
__license__ = "MIT"
__version__ = "0.1"
__python_version__ = "2.7"
__email__ = "jagercox@gmail.com"

IP_SERVER = "0.0.0.0"
PORT_SERVER = 953
TIMEOUT_SOCKET = 10
SIZE_PACKAGE = 4096

IMAGE_HEIGHT = 480
IMAGE_WIDTH = 640
COLOR_PIXEL = 3  # RGB


if __name__ == '__main__':
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection.settimeout(TIMEOUT_SOCKET)
    connection.connect((IP_SERVER, PORT_SERVER))

    while True:
        try:
            fileDescriptor = connection.makefile(mode='rb')
            result = fileDescriptor.readline()
            fileDescriptor.close()
            result = base64.b64decode(result)

            frame = np.fromstring(result, dtype=np.uint8)
            frame_matrix = np.array(frame)
            frame_matrix = np.reshape(frame_matrix, (IMAGE_HEIGHT, IMAGE_WIDTH,
                                                     COLOR_PIXEL))
            cv2.imshow('Window title', frame_matrix)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        except Exception as e:
            print "[Error] " + str(e)

    connection.close()
