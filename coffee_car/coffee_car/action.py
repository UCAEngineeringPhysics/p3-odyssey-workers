import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from geometry_msgs.msg import PoseStamped
from nav2_msgs.action import NavigateToPose

class Nav2ActionClient(Node):
    def __init__(self):
        super().__init__('nav2_action_client')
        self._action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        
        # Variables to remember our goal and track retries
        self.target_x = 0.0
        self.target_y = 0.0
        self.retry_count = 0
        self.max_retries = 3  # Change this to allow more/fewer retries

    def send_goal(self, x, y):
        # Save the targets in case we need to retry
        self.target_x = float(x)
        self.target_y = float(y)
        
        self.get_logger().info('Waiting for action server...')
        self._action_client.wait_for_server()

        # Create the goal message
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose.header.frame_id = 'map'
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
        
        goal_msg.pose.pose.position.x = self.target_x
        goal_msg.pose.pose.position.y = self.target_y
        goal_msg.pose.pose.position.z = 0.0
        goal_msg.pose.pose.orientation.w = 1.0

        self.get_logger().info(f'Sending goal: x={x}, y={y} (Attempt {self.retry_count + 1}/{self.max_retries + 1})')

        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg, 
            feedback_callback=self.feedback_callback
        )
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def feedback_callback(self, feedback_msg):
        distance = feedback_msg.feedback.distance_remaining
        self.get_logger().info(f'Distance remaining: {distance:.2f} meters')

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().warn('Goal was REJECTED by the server.')
            self.handle_failure()
            return

        self.get_logger().info('Goal ACCEPTED! Navigating...')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        status = future.result().status
        
        # Status 4 means SUCCEEDED
        if status == 4:
            self.get_logger().info('Success! The robot reached the destination.')
            rclpy.shutdown()
        else:
            self.get_logger().warn(f'Navigation failed or was canceled. Status code: {status}')
            self.handle_failure()

    def handle_failure(self):
        """Checks if we can retry, and sets up a timer if we can."""
        if self.retry_count < self.max_retries:
            self.retry_count += 1
            self.get_logger().info(f'Retrying in 2 seconds... (Retry {self.retry_count} of {self.max_retries})')
            
            # Use a ROS 2 timer to wait 2 seconds before retrying.
            # This prevents locking up the ROS executor (which time.sleep() would do).
            self.retry_timer = self.create_timer(2.0, self.execute_retry)
        else:
            self.get_logger().error('Max retries reached. Giving up on this goal.')
            rclpy.shutdown()

    def execute_retry(self):
        """Triggered by the timer to actually send the goal again."""
        # Destroy the timer immediately so it only fires once per retry
        self.retry_timer.cancel() 
        self.send_goal(self.target_x, self.target_y)

def main(args=None):
    rclpy.init(args=args)
    action_client = Nav2ActionClient()
    
    # Send the robot to x: 2.0, y: 1.5
    action_client.send_goal(12.5, 14.5)

    rclpy.spin(action_client)

if __name__ == '__main__':
    main()