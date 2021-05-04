import pyrealsense2 as rs
import numpy as np
import cv2
import json
import argparse
import time
import os
import earthpy as et

###############################
# Class definitions:
###############################

class DepthCamera:
    """
    DepthCamera is used handle one single camera.
    """
    def __init__(self, serial_number, stream_settings, output_filepath):
        self.serial_number = serial_number
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.output_filepath = output_filepath


        # Stream settings is a tuple such that: (width[px], height[px], frequency[Hz]).
        self.stream_settings = stream_settings
        
        # Enable all streams we want in the ROSBAG.
        self.config.enable_device(serial_number)
        self.config.enable_stream(rs.stream.color, self.stream_settings[0], self.stream_settings[1], rs.format.bgr8, self.stream_settings[2])

        
        # Enable the recording to ROSBAG.
        timestr = time.strftime("%Y%m%d-%H%M%S")
        filename = self.output_filepath + timestr + "_" + self.serial_number + ".bag"
        self.config.enable_record_to_file(filename)



    def start(self):
        self.pipeline.start(self.config)

    def viz(self):
        frames = self.pipeline.wait_for_frames(20000)  # Increased timeout since it sometimes fail.
        color_frame = frames.get_color_frame()
        
        if not color_frame:
            return
        
        # Convert images to numpy arrays
        color_image = np.asanyarray(color_frame.get_data())

        return color_image

    def stop(self):
        self.pipeline.stop()

class DepthRecorder:
    """
    DepthRecorder is useful to handle several cameras.
    In essence it contains several DepthCamera objects.
    This depends on the number of cameras found by rs.context().
    """
    cameras = []
    images = []

    def __init__(self, json_file, output_filepath):
        self.context = rs.context()
        self.devices = self.context.query_devices()
        self.out_path = et.io.HOME+output_filepath
        self.count = 0


        jsonObj = json.load(open(json_file))
        self.json_payload = str(jsonObj).replace("'", '\"')

        os.chdir(self.out_path)
        timestr = time.strftime("%Y%m%d-%H%M%S")
        os.mkdir(str(timestr))
        os.chdir(str(timestr))

        stream_settings = (int(jsonObj['stream-width']), int(jsonObj['stream-height']), int(jsonObj['stream-fps']))

        # Configure each device according to the YAML file.
        for device in self.devices:
            serial_number = device.get_info(rs.camera_info.serial_number)
            print("Configuring device with serial number: {}".format(serial_number))
            advanced_mode = rs.rs400_advanced_mode(device)
            if(advanced_mode.is_enabled()):
                advanced_mode.load_json(self.json_payload)
            else:
                print("No advance mode available, cannot load config into camera.")

            self.cameras.append(DepthCamera(serial_number, stream_settings, self.out_path))

    def start(self):
        for camera in self.cameras:
            camera.start()

    def viz(self):
        camera_images = []

        for camera in self.cameras:
            image = camera.viz()
            filename = str(camera.serial_number) + "_" + str(self.count) + ".png"
            cv2.imwrite(filename, image)
            camera_images.append(image)
            self.count = self.count+1

        display_images = np.hstack(camera_images)

        # Show images from both cameras
        cv2.namedWindow('RealSense viz', cv2.WINDOW_NORMAL)
        cv2.imshow('RealSense viz', display_images)

        cv2.waitKey(1)

    def stop(self):
        for camera in self.cameras:
            camera.stop()


###############################
# Program actually starts here:
###############################

parser = argparse.ArgumentParser(description="Record depthcamera data to ROSBAG.")
parser.add_argument("-c", "--config", type=str, default="config/depthcam.json",
                    help="Stereo module config file (JSON).")
parser.add_argument("-o", "--output", type=str, default="/Dataset/recordings/",
                    help="Output filepath for the ROSBAG (filename is the serial number of the camera).")

args = parser.parse_args()

if args.config and args.output is None :
    print("wrong usage detected")
    parser.print_help()
    exit(1)

print("Settings:")
print("  JSON config file: {}".format(args.config))
print("  Output path: {}".format(et.io.HOME+args.output))


recorder = DepthRecorder(args.config, args.output)
try:
    recorder.start()
    print("Long-press ESC to stop recording")
    while(cv2.waitKey(1) != 27): # Long-press ESC to exit.
        recorder.viz()



finally:
    recorder.stop()
