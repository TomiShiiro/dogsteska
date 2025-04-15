import sys
from enum import Enum

from unitree_sdk2py.core.channel import ChannelSubscriber, ChannelFactoryInitialize
from unitree_sdk2py.go2.sport.sport_client import SportClient
from unitree_sdk2py.go2.obstacles_avoid.obstacles_avoid_client import ObstaclesAvoidClient
from unitree_sdk2py.go2.image.image_client import ImageClient
from unitree_sdk2py.go2.image.camera_handle import CameraHandle
from unitree_sdk2py.go2.sensor.scan_client import ScanClient

# Constants for obstacle detection
MIN_DISTANCE = 0.5          # Minimum distance to consider as obstacle (meters)
SAFE_DISTANCE = 1.0         # Safe distance from obstacles (meters)
SCAN_ANGLE_MIN = -45.0      # Minimum angle for scan (deg)
SCAN_ANGLE_MAX = 45         # Maximum angle for scan (deg)

# Obstacle representation

class Obstacle:
    def __init__(self, distance: float, angle: float, size: float):
        self.distance = distance    # Distance to obstacle in meters
        self.angle = angle          # Angle to obstacle in degrees
        self.size = size            # Estimated size of obstacle in meters

    def __repr__(self):
        return f"Obstacle(distance={self.distance}, angle={self.angle}, size={self.size})"
    
    def __eq__(self, other):
        if not isinstance(other, Obstacle):
            return NotImplemented
        return (
            self.distance == other.distance and
            self.angle == other.angle and
            self.size == other.size
        )

    def __str__(self):
        return f"Obstacle distance={self.distance:.2f}m, angle={self.angle:.2f}deg, size={self.size:.2f}m"

class DetectionMode(Enum):
    LIDAR = 1   # Using lidar/depth sensors
    CAMERA = 2  # Using camera-based detection
    HYBRID = 3  # Using both lidar and camera

class ObstacleDetector:
    def __init__(self, network_interface=None, detection_mode=DetectionMode.HYBRID):
        """Initialize obstacle detector with specified detection mode"""
        print("Initializing Obstacle Detector...")
        
        # Initialize channel factory
        if network_interface:
            ChannelFactoryInitialize(0, network_interface)
        else:
            ChannelFactoryInitialize(0)

        self.detection_mode = detection_mode
        self.obstacles = []

        # Initialize clients based on detection mode
        self.sport_client = SportClient()
        self.sport_client.SetTimeout(10.0)
        self.sport_client.Init()

        if detection_mode in [DetectionMode.LIDAR, DetectionMode.HYBRID]:
            self.scan_client = ScanClient()
            self.scan_client.SetTimeout(3.0)
            self.scan_client.Init()

        if detection_mode in [DetectionMode.CAMERA, DetectionMode.HYBRID]:
            self.image_client = ImageClient()
            self.image_client.SetTimeout(3.0)
            self.image_client.Init()
            self.camera_handle = CameraHandle.FRONT

        # Initialize obstacle avoidance client
        self.avoid_client = ObstaclesAvoidClient()
        self.avoid_client.SetTimeout(3.0)
        self.avoid_client.Init()
        
        print("Obstacle Detector initialized")

def demo_obstacle_detection(network_interface=None):
    """Demonstrate obstacle detection capabilities"""
    print("Obstacle Detection Demo")
    detector = ObstacleDetector(network_interface, DetectionMode.HYBRID)

    

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python3 {sys.argv[0]} networkInterface")
        print("Running default network interface")
        demo_obstacle_detection()
    else:
        demo_obstacle_detection(sys.argv[1])
