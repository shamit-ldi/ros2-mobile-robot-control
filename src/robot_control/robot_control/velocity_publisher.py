import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped


class VelocityPublisher(Node):

    def __init__(self):
        super().__init__('velocity_publisher')

        self.publisher_ = self.create_publisher(
            TwistStamped,
            '/cmd_vel',
            10
        )

        self.timer = self.create_timer(
            0.1,
            self.publish_velocity
        )

        self.get_logger().info('Velocity Publisher started')

    def publish_velocity(self):
        msg = TwistStamped()

        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'

        msg.twist.linear.x = 0.2
        msg.twist.angular.z = 0.2

        self.publisher_.publish(msg)

        self.get_logger().info(
            f'Publishing: linear={msg.twist.linear.x}, '
            f'angular={msg.twist.angular.z}'
        )


def main(args=None):
    rclpy.init(args=args)

    node = VelocityPublisher()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
