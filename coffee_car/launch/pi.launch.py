import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    # 1. Get the path to your 'proj2' package share directory
    coffee_car_share_dir = get_package_share_directory('coffee_car')
    
    # 2. Build the exact path to your ekf.yaml file
    ekf_config_path = os.path.join(coffee_car_share_dir, 'config', 'ekf.yaml')

    # 3. Get the path to the rplidar_ros launch file
    rplidar_share_dir = get_package_share_directory('rplidar_ros')
    rplidar_launch_file = os.path.join(rplidar_share_dir, 'launch', 'rplidar.launch.py') #from rplidar.launch.py

    return LaunchDescription([
        # Your custom nodes (ensure these names match the console_scripts in setup.py)
        Node(
            package='coffee_car',
            executable='subpub',
            name='subpub_node'
        ),
        
        # CORRECT WAY to include another launch file
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(rplidar_launch_file)
        ),
        
        # Laser Scan Matcher Node
        Node(
            package="ros2_laser_scan_matcher",
            executable="laser_scan_matcher",
            name="laser_scan_matcher_node",
            parameters=[{
                "publish_tf": False,
                "publish_odom": "/laser_odom",
                "laser_frame": "laser",
                "max_iterations": 10,
            }]
        ),
        
        # EKF Node passing the absolute path to the YAML file
        Node(
            package="robot_localization",
            executable="ekf_node",
            name="ekf_filter_node",
            parameters=[ekf_config_path]
        ),

        ExecuteProcess(
            cmd = [
                "ros2", "bag", "record", "-o", "data", "/imu_pub", "/odom_pub", "/odometry/filtered"
            ]
        )
    ])