import time
import sys
import os
import numpy as np
import cv2
import math
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Tuple, Dict
import json


from unitree_sdk2py.core.channel import ChannelFactoryInitialize
from unitree_sdk2py.go2.sport.sport_client import SportClient

from detekce import ObstacleDetector, DetectionMode

@dataclass
class MapPoint:
    """Representation of a point on the map"""
    id: int
    name: str
    x: float
    y: float
    description: str = ""

    def __str__(self):
        return f"Point {self.id}: {self.name} at coordinates {self.x:.2f}, {self.y:.2f}"
    
class MapVisualizer:
    """Class for map visualization"""
    def __init__(self, width=800, height=600, pixel_per_meter=50):
        self.width = width
        self.height = height
        self.pixel_per_meter = pixel_per_meter
        self.center_x = width // 2
        self.center_y = height // 2

    def create_map_image(self, map_points: List[MapPoint], current_position: Tuple[float, float] = (0, 0), obstacles: List = None):
        """Create a map image with points and obstacles"""

        # Create empty image
        img = np.ones((self.height, self.width, 3), dtype=np.uint8) * 255

        # Draw grid
        self.draw_grid(img)

        if obstacles:
            self.draw_obstacles(img, obstacles, current_position)

        # Draw current position
        current_x_px = self.center_x + int(current_position[0] * self.pixel_per_meter)
        current_y_px = self.center_y - int(current_position[1] * self.pixel_per_meter)
        cv2.circle(img, (current_x_px, current_y_px), 10, (0, 0, 255), -1) # Red dot
        cv2.putText(img, "DOG", (current_x_px + 15, current_y_px), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        # Draw all points
        for point in map_points:
            x_px = self.center_x + int(point.x * self.pixel_per_meter)
            y_px = self.center_y - int(point.y * self.pixel_per_meter) # Invert y-axis

            # Draw point
            cv2.circle(img, (x_px, y_px), 8, (0, 128, 0), -1) # Green dot

            # Draw ID and name of point
            cv2.putText(img, f"{point.id}: {point.name}", (x_px + 10, y_px - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
            

        return img
    
    def draw_grid(self, img):
        """Draws grid on the map"""
        # Draw main axes
        cv2.line(img, (0, self.center_y), (self.width, self.center_y), (200, 200, 200), 2)  # X axis
        cv2.line(img, (self.center_x, 0), (self.center_x, self.height), (200, 200, 200), 2)  # Y axis
        
        # Draw meter marks
        for i in range(-10, 11):
            if i == 0:
                continue
            # Marks on X axis
            x_px = self.center_x + i * self.pixels_per_meter
            if 0 <= x_px < self.width:
                cv2.line(img, (x_px, self.center_y - 5), (x_px, self.center_y + 5), (150, 150, 150), 1)
                cv2.putText(img, f"{i}m", (x_px - 10, self.center_y + 20), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (100, 100, 100), 1)
            
            # Marks on Y axis
            y_px = self.center_y - i * self.pixels_per_meter
            if 0 <= y_px < self.height:
                cv2.line(img, (self.center_x - 5, y_px), (self.center_x + 5, y_px), (150, 150, 150), 1)
                cv2.putText(img, f"{i}m", (self.center_x + 10, y_px + 5), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (100, 100, 100), 1)
    
    def draw_obstacles(self, img, obstacles, current_position):
        """Draws obstacles on the map"""
        current_x, current_y = current_position
        current_x_px = self.center_x + int(current_x * self.pixels_per_meter)
        current_y_px = self.center_y - int(current_y * self.pixels_per_meter)
        
        for obstacle in obstacles:
            # Convert polar coordinates to cartesian
            angle_rad = math.radians(obstacle.angle)
            obs_x = current_x + obstacle.distance * math.cos(angle_rad)
            obs_y = current_y + obstacle.distance * math.sin(angle_rad)
            
            # Convert to pixels
            obs_x_px = self.center_x + int(obs_x * self.pixels_per_meter)
            obs_y_px = self.center_y - int(obs_y * self.pixels_per_meter)
            
            # Draw obstacle
            size_px = max(int(obstacle.size * self.pixels_per_meter), 5)
            cv2.circle(img, (obs_x_px, obs_y_px), size_px, (0, 0, 255), 2)
            
            # Draw line from current position to obstacle
            cv2.line(img, (current_x_px, current_y_px), (obs_x_px, obs_y_px), (200, 200, 200), 1)