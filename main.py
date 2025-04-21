import sys

import cv2
import numpy as np
import asyncio

from detekce import ObstacleDetector
from unitree_sdk2py.go2.video.video_client import VideoClient
from queue import Queue

class Map:
    def __init__(self):
        pass        
    def GetPosition(self):
        pass

class Destination:
    """ 
        Args:
        - x: Body x-direction speed command, limited to -1.5~+1.5(m/s);
        - y: Body y-direction speed command, limited to -1~+1(m/s);
        - yaw: Body yaw angular velocity command, limited to -1.57~+1.57(rad/s).
    """
    def __init__(self, x: float, y:float, yaw:float):
        self.x = x
        self.y = y
        self.yaw = yaw

    def __str__(self):
        return f"x = {self.x}m/s | y = {self.y}m/s | angular velocity = {self.yaw}rad/s"



class Dogsteska:
    def __init__(self, network_interface=None):
        self.avoidance = ObstacleDetector(network_interface).avoid_client
        self.map = Map() #TODO mapa, systém koordinace
        self.start_position = self.map.GetPosition()
        
        self.avoidance.SwitchSet(True) # turn on obstacle detection
        
        self.video_client = VideoClient()
        self.frame_queue = Queue()
    
        
    def Move(self, x:float, y:float, yaw:float):
        """ 
            Moves Dogsteska with obstacle avoidance

            Args:
            - x (float): The target position's x-coordinate in meters.
            - y (float): The target position's y-coordinate in meters.
            - yaw (float): The desired orientation in radians, where 0 corresponds to facing forward.

            Example:
            >>> Move(1.0, 0.0, 0.0)
        """
        self.avoidance.UseRemoteCommandFromApi(True)
        self.avoidance.Move(x, y, yaw)
        # TODO zjistit kdy movement skončil
        self.avoidance.UseRemoteCommandFromApi(False)
        
        
    async def GetToDestination(self, code:tuple[float, float, float]):
        x, y, yaw = code
        self.Move(x, y, yaw)
        
    async def ReturnToStart(self):
        x, y, yaw = self.start_position
        self.Move(x, y, yaw)

    async def ScanCode(self) -> tuple[float, float, float]:
        #TODO vrátí x, y, yaw podle custom mapy? 
        return (0, 0, 0)
    
    def GetFrame(self):
        code, data = self.video_client.GetImageSample()
        
        if code == 0:
            image_data = np.frombuffer(bytes(data), dtype=np.uint8)
      
            if image_data is None:
                return None
                        
            frame = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
            return frame

        return None
    async def video_stream_thread(self):
        try:
            while True:
                frame = self.GetFrame()
                
                if(frame is None):
                    await asyncio.sleep(0.01)
                    continue
                    
                self.frame_queue.put(frame)
        except Exception as e:
            print("Error in Video thread")
            print(e)
    
    async def dogsteska_control_thread(self):
        try:
            await self.ReturnToStart() # Start from default position
            
            while True:         
                code = None
                while not code:
                    code = await self.ScanCode()
                    pass  
                
                await self.GetToDestination(code)
                await self.ReturnToStart()
        except Exception as e:
            print("Error in Control thread")
            print(e)

def main():    
    print("Initializing main")
    if len(sys.argv) < 2:
        dogsteska = Dogsteska() 
    else:
        dogsteska = Dogsteska(sys.argv[1]) 
    
    print("Initializing threads")
    control_task = asyncio.to_thread(dogsteska.dogsteska_control_thread())
    video_task = asyncio.to_thread(dogsteska.video_stream_thread())
    
    try:
        while True:
            if not dogsteska.frame_queue.empty():
                frame = dogsteska.frame_queue.get()
                cv2.imshow('Video Stream', frame)

            if cv2.waitKey(1) == ord('q'):
                print("User is quitting")
                break
    except Exception as e:
        print("Error in main thread")
        print(e)
    finally:
        print("Shutting down")
        control_task.close()
        video_task.close()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()