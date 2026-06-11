"""Simple String publisher node for workspace smoke tests."""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Publisher(Node):
    """Publish incrementing messages on my_first_pkg_topic."""

    def __init__(self):
        super().__init__('publisher')
        self.publisher = self.create_publisher(String, 'my_first_pkg_topic', 10)
        self.counter = 0
        self.timer = self.create_timer(1.0, self.publish_message)

    def publish_message(self):
        message = String()
        message.data = 'bonjour ROS2! && ' + str(self.counter)
        self.publisher.publish(message)
        self.get_logger().info("Publishing: 'my_first_pkg_topic' message")
        self.counter += 1


def main(args=None):
    rclpy.init(args=args)
    newnode = Publisher()

    try:
        rclpy.spin(newnode)
    except KeyboardInterrupt:
        pass
    finally:
        newnode.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
