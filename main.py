import sys

import cv2
import numpy as np
import asyncio

from detekce import ObstacleDetector
from unitree_sdk2py.go2.video.video_client import VideoClient
from queue import Queue

class Dogsteska:
    def __init__(self, network_interface=None):
        self.avoidance = ObstacleDetector(network_interface).avoid_client
        self.map = None #TODO mapa, systém koordinace
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
        while True:
            frame = await self.GetFrame()
            
            if(frame is None):
                await asyncio.sleep(0.01)
                continue
                
            self.frame_queue.put(frame)
    
    async def dogsteska_control_thread(self):
        await self.ReturnToStart() # Start from default position
            
        while True:         
            code = None
            while not code:
                code = await self.ScanCode()
                pass  
            
            await self.GetToDestination(code)
            await self.ReturnToStart()

async def main():    
    if len(sys.argv) < 2:
        dogsteska = Dogsteska() 
    else:
        dogsteska = Dogsteska(sys.argv[1]) 
    
    control_task = asyncio.create_task(dogsteska.dogsteska_control_thread())
    video_task = asyncio.create_task(dogsteska.video_stream_thread())
    
    try:
        while True:
            if not dogsteska.frame_queue.empty():
                frame = dogsteska.frame_queue.get()
                cv2.imshow('Video Stream', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            await asyncio.sleep(0.01)  # Let the loop breathe a bit
    finally:
        control_task.cancel()
        video_task.cancel()
        await asyncio.gather(control_task, video_task, return_exceptions=True)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    asyncio.run(main())