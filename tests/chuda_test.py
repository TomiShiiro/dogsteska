import time
import sys
from unitree_sdk2py.go2.obstacles_avoid.obstacles_avoid_client import ObstaclesAvoidClient


def walk(howLong:int):
    try:
        moveClient = ObstaclesAvoidClient()
        moveClient.SetTimeout(3.0)
        moveClient.Init()

        while not moveClient.SwitchGet()[1]:
            moveClient.SwitchSet(True)
            time.sleep(0.1)

        print("obstacles avoid switch on")

        moveClient.UseRemoteCommandFromApi(True)
        time.sleep(0.5)
        moveClient.Move(1, 0.0, 0.0)
        time.sleep(howLong) # move 1s
        moveClient.Move(0.0, 0.0, 0.0)
        moveClient.UseRemoteCommandFromApi(False)

    except KeyboardInterrupt:
        moveClient.Move(0.0, 0.0, 0.0)
        moveClient.UseRemoteCommandFromApi(False)
        print("exit!!")
