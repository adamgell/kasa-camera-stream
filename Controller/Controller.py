import os
import sys
import json
import Wrapper
import asyncio
import requests
import HealthChecker
from concurrent.futures import ThreadPoolExecutor
import socket

class Controller:
    def loadConfiguration(self, path):
        print("[Controller] Loading configuration.")
        with open(path) as configFile:
            master_config = json.load(configFile)
            
            # Get container hostname which will match camera name
            hostname = socket.gethostname()
            camera_name = hostname.split('-')[-1]  # gets 'backyard' from 'kasa-camera-backyard'
            
            print(f"[Controller] Looking for config for camera: {camera_name}")
            
            # Find matching camera config
            camera_config = None
            for camera in master_config['cameras']:
                if camera['cameraname'] == camera_name:
                    camera_config = camera
                    break
                    
            if not camera_config:
                raise Exception(f"No configuration found for camera {camera_name}")
                
            # Combine master and camera configs
            config = {
                'kasausername': master_config['kasausername'],
                'kasapassword': master_config['kasapassword'],
                'cameraip': camera_config['cameraip'],
                'cameraname': camera_config['cameraname']
            }
            
            print(f"[Controller] Loaded configuration for camera: {config['cameraname']}")
            return config

    def run(self):
        print("[Controller] Controller is starting.")

        # Set variables
        self.config = self.loadConfiguration("/data/master.json")

        # Create Ffmpeg wrapper
        self.ffmpegWrapper = Wrapper.FfmpegWrapper(self, 10)
        self.ffmpegWrapper.startProcess()

        # Start tasks
        loop = asyncio.get_event_loop()

        print("[Controller] Controller is running.")
        loop.run_forever()
        print("[Controller] Exiting.")

def main():
   controller = Controller()
   controller.run()

if __name__ == '__main__':
    main()