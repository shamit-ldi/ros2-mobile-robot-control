import rclpy
from rclpy.node import Node

from geometry_msgs.msg import TwistStamped
from nav_msgs.msg import Odometry

import math


class PointController(Node):

    def __init__(self):
        super().__init__('point_controller')

        # Target position
        self.x_goal = 2.0
        self.y_goal = 1.0

        # Controller gains
        self.k_v = 0.4
        self.k_omega = 1.5

        # Maximum velocities
        self.max_linear_velocity = 0.22
        self.max_angular_velocity = 1.0

        # Goal tolerance
        self.goal_tolerance = 0.05

        # Current robot state
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        self.odom_received = False

        # Subscribe to odometry
        self.subscription = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10
        )

        # Publish velocity commands
        self.publisher = self.create_publisher(
            TwistStamped,
            '/cmd_vel',
            10
        )

        # Run controller at 10 Hz
        self.timer = self.create_timer(
            0.1,
            self.control_loop
        )

        self.get_logger().info(
            f'Point Controller started. '
            f'Goal = ({self.x_goal:.2f}, {self.y_goal:.2f})'
        )

    def odom_callback(self, msg):

        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y

        qz = msg.pose.pose.orientation.z
        qw = msg.pose.pose.orientation.w

        self.theta = 2.0 * math.atan2(qz, qw)

        self.odom_received = True

    def normalize_angle(self, angle):

        while angle > math.pi:
            angle -= 2.0 * math.pi

        while angle < -math.pi:
            angle += 2.0 * math.pi

        return angle

    def control_loop(self):

        if not self.odom_received:
            return

        # Position error
        dx = self.x_goal - self.x
        dy = self.y_goal - self.y

        distance_error = math.sqrt(dx**2 + dy**2)

        # Desired heading
        desired_theta = math.atan2(dy, dx)

        # Heading error
        heading_error = self.normalize_angle(
            desired_theta - self.theta
        )

        msg = TwistStamped()

        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'

        # Stop when target is reached
        if distance_error < self.goal_tolerance:

            msg.twist.linear.x = 0.0
            msg.twist.angular.z = 0.0

            self.publisher.publish(msg)

            self.get_logger().info(
                f'GOAL REACHED: x={self.x:.3f}, y={self.y:.3f}'
            )

            return

        # Proportional controller
        linear_velocity = self.k_v * distance_error
        angular_velocity = self.k_omega * heading_error

        # Velocity saturation
        linear_velocity = min(
            linear_velocity,
            self.max_linear_velocity
        )

        angular_velocity = max(
            -self.max_angular_velocity,
            min(angular_velocity, self.max_angular_velocity)
        )

        msg.twist.linear.x = linear_velocity
        msg.twist.angular.z = angular_velocity

        self.publisher.publish(msg)

        self.get_logger().info(
            f'Position=({self.x:.2f}, {self.y:.2f}) | '
            f'Distance error={distance_error:.2f} | '
            f'Heading error={heading_error:.2f} | '
            f'v={linear_velocity:.2f} | '
            f'omega={angular_velocity:.2f}'
        )


def main(args=None):

    rclpy.init(args=args)

    node = PointController()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    node.destroy_node()

    if rclpy.ok():
        rclpy.shutdown()


if __name__ == '__main__':
    main()
