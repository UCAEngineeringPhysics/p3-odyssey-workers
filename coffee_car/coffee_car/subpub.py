import rclpy
from rclpy.node import Node


from geometry_msgs.msg import Twist, TransformStamped
from sensor_msgs.msg import LaserScan, Imu
from nav_msgs.msg import Odometry

from tf_transformations import quaternion_about_axis
import serial
import math
from tf2_ros.static_transform_broadcaster import StaticTransformBroadcaster
from tf2_ros.buffer import Buffer


class subscriber(Node):
    def __init__(self):
        super().__init__("subscriber")
        self.declare_parameter("robot_name", 'nugget')
        robot_name = self.get_parameter('robot_name').get_parameter_value().string_value

        self.curr_ts = self.get_clock().now()
        self.prev_ts = self.get_clock().now()
    
        
        self.pico_msngr =  serial.Serial("/dev/ttyACM0", 115200, timeout=0.01)
        self.listen_pico_msg_timer = self.create_timer(0.02, self.listen_pico_msg)

        self.broadcaster = StaticTransformBroadcaster(self)

        self.vel_subscriber = self.create_subscription(
            msg_type=Twist,
            topic="cmd_vel",
            qos_profile=1,
            callback=self.set_target_vel
        )

        self.odom_publisher = self.create_publisher(
            msg_type= Odometry,
            topic="odom_pub",
            qos_profile=1
        )

        self.imu_publisher = self.create_publisher(
            msg_type=Imu,
            topic = "imu_pub",
            qos_profile=1

        )

        self.targ_lin_vel = 0.0
        self.targ_ang_vel = 0.0
        self.lin_vel = 0.0
        self.ang_vel = 0.0
        self.x_accel = 0.0
        self.y_accel = 0.0
        self.z_accel = 0.0
        self.omeg_x = 0.0 #angular vel
        self.omeg_y = 0.0
        self.omeg_z = 0.0
        self.theta = 0.0
        self.x = 0.0
        self.y = 0.0

        lidar = TransformStamped()
        lidar.header.stamp=self.get_clock().now().to_msg()
        lidar.header.frame_id = "base_link"
        lidar.child_frame_id = "laser"
        lidar.transform.translation.x = 0.0
        lidar.transform.translation.y = 0.0
        lidar.transform.translation.z = 0.2
        lidar.transform.rotation.x = 0.0
        lidar.transform.rotation.y = 0.0
        lidar.transform.rotation.z = 0.0
        lidar.transform.rotation.w = 1.0
        self.broadcaster.sendTransform(lidar)
        
    def listen_pico_msg(self):
        if self.pico_msngr.inWaiting() > 0:
            data = (
                self.pico_msngr.readline().decode("utf-8", "ignore").strip().split(",")
            )  # actual linear and angular vel
            if len(data) == 8:
                try:
                    self.lin_vel = float(data[0])
                    self.ang_vel = float(data[1])
                    self.x_accel = float(data[2])
                    self.y_accel = float(data[3])
                    self.z_accel = float(data[4])
                    self.omeg_x = float(data[5])
                    self.omeg_y = float(data[6])
                    self.omeg_z = float(data[7])
                except ValueError:
                    self.lin_vel = 0.0
                    self.ang_vel = 0.0
                    self.x_accel = 0.0
                    self.y_accel = 0.0
                    self.z_accel = 0.0
                    self.omeg_x = 0.0
                    self.omeg_y = 0.0
                    self.omeg_z = 0.0

            self.odom_callback()
            self.imu_callback()
        self.get_logger().debug(
            f"Measured velocity\nlinear: {self.lin_vel}, angular: {self.ang_vel}")

    def set_target_vel(self, msg):
        self.targ_lin_vel = msg.linear.x
        self.targ_ang_vel = msg.angular.z
        self.pico_msngr.write(f"{self.targ_lin_vel},{self.targ_ang_vel}\n".encode("utf-8"))
        self.get_logger().debug(
            f"Set HomeR's target velocity\nlinear: {self.targ_lin_vel}, angular: {self.targ_ang_vel}"
        )
    def imu_callback(self):
        msg = Imu()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "base_link"
        msg.linear_acceleration.x = self.x_accel
        msg.angular_velocity.z = self.omeg_z
        # 1. Orientation (You aren't calculating orientation here, so we tell the EKF to ignore it)
        msg.orientation_covariance = [0.0] * 9
        msg.orientation_covariance[0] = -1.0 # -1.0 is the ROS standard for "no data here"
        
        # 2. Linear Acceleration
        lin_accel_cov = [0.0] * 9
        lin_accel_cov[0] = 0.01  # X 
        lin_accel_cov[4] = 0.01  # Y 
        lin_accel_cov[8] = 0.01  # Z 
        msg.linear_acceleration_covariance = lin_accel_cov
        
        # 3. Angular Velocity
        ang_vel_cov = [0.0] * 9
        ang_vel_cov[0] = 0.01  # X
        ang_vel_cov[4] = 0.01  # Y
        ang_vel_cov[8] = 0.01  # Z (Yaw rate)
        msg.angular_velocity_covariance = ang_vel_cov
        self.imu_publisher.publish(msg)

    def odom_callback(self):
        self.curr_ts = self.get_clock().now()
        dt = (self.curr_ts - self.prev_ts).nanoseconds * 1e-9
        dx = self.lin_vel * math.cos(self.theta) * dt
        dy = self.lin_vel * math.sin(self.theta) * dt
        self.x += dx
        self.y += dy
        dtheta  = self.ang_vel * dt
        self.theta += dtheta
        quat = quaternion_about_axis(self.theta, (0,0,1))
        #qw = math.cos(self.theta / 2.0)
        #qx = 0.0
        #qy = 0.0
        #qz = math.sin(self.theta / 2.0)
        self.prev_ts = self.curr_ts
        msg = Odometry()
        msg.header.stamp = self.curr_ts.to_msg()
        msg.header.frame_id = "odom"
        msg.child_frame_id = "base_link"
        msg.pose.pose.orientation.x = quat[0]
        msg.pose.pose.orientation.y = quat[1]
        msg.pose.pose.orientation.z = quat[2]
        msg.pose.pose.orientation.w = quat[3]
        #msg.pose.pose.orientation.x = qx
        #msg.pose.pose.orientation.y = qy
        #msg.pose.pose.orientation.z = qz
        #msg.pose.pose.orientation.w = qw
        msg.pose.pose.position.x = self.x
        msg.pose.pose.position.y = self.y
        msg.pose.pose.position.z = 0.325
        msg.twist.twist.linear.x = self.lin_vel
        msg.twist.twist.angular.z = self.ang_vel

        # 1. Pose Covariance (Position & Orientation)
        pose_cov = [0.0] * 36
        pose_cov[0] = 0.01   # X
        pose_cov[7] = 0.01   # Y
        pose_cov[35] = 0.05  # Yaw
        msg.pose.covariance = pose_cov
        
        # 2. Twist Covariance (Linear & Angular Velocity)
        twist_cov = [0.0] * 36
        twist_cov[0] = 0.01  # Linear X
        twist_cov[7] = 0.01  # Linear Y
        twist_cov[35] = 0.05 # Angular Z (Yaw rate)
        msg.twist.covariance = twist_cov

        self.odom_publisher.publish(msg)

    
def main(args=None):
    rclpy.init(args=args)
    node = subscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()