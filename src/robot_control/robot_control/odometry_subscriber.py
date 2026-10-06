import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
import math


class OdometrySubscriber(Node):

    def __init__(self):
        super().__init__('odometry_subscriber')

        self.subscription = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10
        )

        self.get_logger().info('Odometry Subscriber started')

    def odom_callback(self, msg):

        # Position
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y

        # Quaternion orientation
        qz = msg.pose.pose.orientation.z
        qw = msg.pose.pose.orientation.w

        # Convert quaternion to yaw for planar motion
        theta = 2.0 * math.atan2(qz, qw)

        self.get_logger().info(
            f'x={x:.3f} m, y={y:.3f} m, theta={theta:.3f} rad'
        )


def main(args=None):
    rclpy.init(args=args)

    node = OdometrySubscriber()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()

    if rclpy.ok():
        rclpy.shutdown()


if __name__ == '__main__':
    main()
