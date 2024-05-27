#!/usr/bin/env python3

# import rclpy
# from rclpy.node import Node
# from sensor_msgs.msg import Image
# from cv_bridge import CvBridge
# import cv2

# class CameraPublisher(Node):

#     def __init__(self):
#         super().__init__('camera_publisher')
#         self.publisher_ = self.create_publisher(Image, 'camera', 10)
#         self.timer = self.create_timer(0.1, self.timer_callback)
#         self.bridge = CvBridge()
#         self.cap = cv2.VideoCapture(2)
#         print('Camera Publisher Node has been started')
#         print("Resolution: " + str(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)) + " x " + str(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

#     def timer_callback(self):
#         ret, frame = self.cap.read()
#         if ret:
#             msg = self.bridge.cv2_to_imgmsg(frame, 'bgr8')
#             msg.header.stamp = self.get_clock().now().to_msg()  # Set the current time as the timestamp
#             self.publisher_.publish(msg)

# def main(args=None):
#     rclpy.init(args=args)
#     camera_publisher = CameraPublisher()
#     rclpy.spin(camera_publisher)
#     camera_publisher.destroy_node()
#     rclpy.shutdown()

# if __name__ == '__main__':
#     main()


import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import os
import time

class CameraPublisher(Node):
    def __init__(self):
        super().__init__('image_publisher')
        self.publisher_ = self.create_publisher(Image, 'camera', 10)
        self.timer = self.create_timer(0.1, self.timer_callback)  # Adjust the timer interval as needed
        self.bridge = CvBridge()
        self.image_folder = '/home/kool/Dev/EDI_WS/sequence_02/images/'  # Update this path to your images folder
        self.images = sorted(os.listdir(self.image_folder))
        print('Camera Publisher Node has been started')
        # sleep for 20 seconds to allow the subscriber to connect
        self.get_logger().info('Sleeping for 20 seconds...')
        time.sleep(20)
        self.get_logger().info('Done sleeping')

    def timer_callback(self):
        
        if len(self.images) > 0:
            img_path = os.path.join(self.image_folder, self.images.pop(0))  # Load the next image
            frame = cv2.imread(img_path)
            if frame is not None:
                msg = self.bridge.cv2_to_imgmsg(frame, 'bgr8')
                msg.header.stamp = self.get_clock().now().to_msg()  # Set the current time as the timestamp
                self.publisher_.publish(msg)
            else:
                print(f"Failed to load image {img_path}")

def main(args=None):
    rclpy.init(args=args)
    camera_publisher = CameraPublisher()
    rclpy.spin(camera_publisher)
    camera_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
