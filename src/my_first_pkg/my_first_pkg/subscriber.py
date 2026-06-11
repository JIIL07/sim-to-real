import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Subscriber(Node):
    def __init__(self):
        super().__init__('subscriber')
        self.subscription = self.create_subscription(String, 'my_first_pkg_topic', self.listener_callback, 10)
    def listener_callback(self, message):
        self.get_logger().info(f"Received message: {message.data}")


def main(args=None):
    rclpy.init(args=args)
    node = Subscriber()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

# Сдвинуто к левому краю
if __name__ == '__main__':
    main()