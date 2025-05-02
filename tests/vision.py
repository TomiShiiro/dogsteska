from unitree_sdk2py.core.channel import ChannelFactoryInitialize
from unitree_sdk2py.go2.video.video_client import VideoClient
import cv2
import numpy as np
import sys
import time
from pyzbar import pyzbar

from chuda_test import walk


if len(sys.argv)>1:
    ChannelFactoryInitialize(0, sys.argv[1])
else:
    ChannelFactoryInitialize(0)

client = VideoClient()  # Create a video client
client.SetTimeout(3.0)
client.Init()

code, data = client.GetImageSample()
qr_code_found = False

# Request normal when code==0
while True: #code == 0 and not qr_code_found:
    # Get Image data from Go2 robot
    code, data = client.GetImageSample()

    # Convert to numpy image
    image_data = np.frombuffer(bytes(data), dtype=np.uint8)
    image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

     # Convert frame to grayscale (QR detection works better with grayscale)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    barcodes = pyzbar.decode(gray)
    
    for barcode in barcodes:
        barcode_data = barcode.data.decode("utf-8")
        barcode_type = barcode.type
        print(f"Found {barcode_type} QR Code: {barcode_data}")

        # Put guidance function here, use param barcode_data
        time.sleep(2)   # keep here so user has time to lift phone out the way

        
        
        qr_code_found = True
        break  
    
    # Display the camera output (comment out if not needed)
    cv2.imshow('front_camera', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

if code != 0:
    print("Get image sample error. code:", code)


cv2.destroyWindow("front_camera")