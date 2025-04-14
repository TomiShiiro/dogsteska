import time
import sys
from unitree_sdk2py.core.channel import ChannelSubscriber, ChannelFactoryInitialize
from unitree_sdk2py.idl.default import unitree_go_msg_dds__SportModeState_
from unitree_sdk2py.idl.unitree_go.msg.dds_ import SportModeState_
from unitree_sdk2py.go2.sport.sport_client import (
    SportClient,
    PathPoint,
    SPORT_PATH_POINT_SIZE,
)
import math
from dataclasses import dataclass

if len(sys.argv) < 2:
    print(f"Usage: python3 {sys.argv[0]} networkInterface")
    sys.exit(-1)

print("WARNING: Please ensure there are no obstacles around the robot while running this example.")


ChannelFactoryInitialize(0, sys.argv[1])


sport_client = SportClient()  
sport_client.SetTimeout(10.0)
sport_client.Init()


#rotate = input("PKOlik: ")
#sport_client.Move(0,0,float(rotate))
for i in range(7):
    sport_client.Move(0,0,float(2))
    time.sleep(0.5)