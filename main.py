import sys

from detekce import ObstacleDetector

class Dogsteska:
    def __init__(self, network_interface=None):
        self.avoidance = ObstacleDetector(network_interface).avoid_client
        self.map = None #TODO mapa, systém koordinace
        self.start_position = self.map.GetPosition()
        
        self.avoidance.SwitchSet(True) # turn on obstacle detection
    
        
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
        
        
    def GetToDestination(self, code:tuple[float, float, float]):
        x, y, yaw = code
        self.Move(x, y, yaw)
        
    def ReturnToStart(self):
        x, y, yaw = self.start_position
        self.Move(x, y, yaw)

    def ScanCode(self) -> tuple[float, float, float]:
        #TODO vrátí x, y, yaw podle custom mapy? 
        return (0, 0, 0)



if __name__ == "__main__":
    if len(sys.argv) < 2:
        dogsteska = Dogsteska() 
    else:
        dogsteska = Dogsteska(sys.argv[1]) 
    
    dogsteska.ReturnToStart() # Start from default position
        
    while True:         
        code = None
        while not code:
            code = dogsteska.ScanCode()
            pass  
        
        dogsteska.GetToDestination(code)
        dogsteska.ReturnToStart()