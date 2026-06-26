import sys
import rclpy
from witmotion import IMU
import math
from rclpy.node import Node
from sensor_msgs.msg import Imu

PORT = '/dev/ttyUSB0'
BAUD = 38400

def converter(accel, gyro, angle):
    #converting from g to m/s^2
    accel_ms2 = {
        'x': accel[0],
        'y': accel[1],
        'z': accel[2]
    }
    #converting degrees to radians
    gyro_rads = {
        'x': math.radians(gyro[0]),
        'y': math.radians(gyro[1]),
        'z': math.radians(gyro[2])
    }
    #converting degrees to quaternions
    roll = math.radians(angle[0])
    pitch = math.radians(angle[1])
    yaw = math.radians(angle[2])

    qx = math.sin(roll / 2) * math.cos(pitch / 2) * math.cos(yaw / 2) - math.cos(roll / 2) * math.sin(pitch / 2) * math.sin(yaw / 2)
    qy = math.cos(roll / 2) * math.sin(pitch / 2) * math.cos(yaw / 2) + math.sin(roll / 2) * math.cos(pitch / 2) * math.sin(yaw / 2)
    qz = math.cos(roll / 2) * math.cos(pitch / 2) * math.sin(yaw / 2) - math.sin(roll / 2) * math.sin(pitch / 2) * math.cos(yaw / 2)
    qw = math.cos(roll / 2) * math.cos(pitch / 2) * math.cos(yaw / 2) + math.sin(roll / 2) * math.sin(pitch / 2) * math.sin(yaw / 2)

    quaternion = {'x': qx, 'y': qy, 'z': qz, 'w': qw}

    return {
        'linear_acceleration': accel_ms2,
        'angular_velocity': gyro_rads,
        'orientation': quaternion
    }

class IMU_Node(Node):
    def __init__(self, PORT, BAUD):
        super().__init__("imu_node")
        self.publisher = self.create_publisher(Imu, '/imu/data_raw', 10)

        try:
            self.imu = IMU(path=PORT, baudrate=BAUD)
        except Exception:
            sys.exit(1)

        self.timer = self.create_timer(0.05, self.timer_callback)

    def timer_callback(self):
        accel = self.imu.get_acceleration()
        gyro = self.imu.get_angular_velocity()
        angle = self.imu.get_angle()

        if accel is None or gyro is None or angle is None:
            return

        data = converter(accel, gyro, angle)
        #converting data to datatype in ros2 IMU
        msg = Imu()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'imu_link'

        msg.linear_acceleration.x = data['linear_acceleration']['x']
        msg.linear_acceleration.y = data['linear_acceleration']['y']
        msg.linear_acceleration.z = data['linear_acceleration']['z']

        msg.angular_velocity.x = data['angular_velocity']['x']
        msg.angular_velocity.y = data['angular_velocity']['y']
        msg.angular_velocity.z = data['angular_velocity']['z']

        msg.orientation.x = data['orientation']['x']
        msg.orientation.y = data['orientation']['y']
        msg.orientation.z = data['orientation']['z']
        msg.orientation.w = data['orientation']['w']

        self.publisher.publish(msg)

def main():
    rclpy.init()
    node = IMU_Node(PORT, BAUD)
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if hasattr(node, 'imu'):
            node.imu.close()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()