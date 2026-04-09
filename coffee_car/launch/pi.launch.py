import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    # 1. Get the path to your 'proj2' package share directory
    coffee_car_share_dir = get_package_share_directory('coffee_car')
    
    # 2. Build the exact path to your ekf.yaml file
    ekf_config_path = os.path.join(coffee_car_share_dir, 'config', 'ekf_no_laser.yaml')


    sim_time_arg = DeclareLaunchArgument(
        name="use_sim_time",
        default_value="false",
        choices=["true", "false"],
        description="Flag to enable use simulation time",
    )

    return LaunchDescription([
        sim_time_arg,
        # Your custom nodes (ensure these names match the console_scripts in setup.py)
        Node(
            package='coffee_car',
            executable='subpub',
            name='subpub_node'
        ),
        
       Node(
            name='rplidar_composition',
            package='rplidar_ros',
            executable='rplidar_composition',
            output='screen',
            parameters=[{
                'serial_port': '/dev/ttyUSB0',
                'serial_baudrate': 115200,  # A1 / A2
                # 'serial_baudrate': 256000, # A3
                'frame_id': 'lidar_link',
                'inverted': False,
                'angle_compensate': True,
            }],
        ),
        
        # Laser Scan Matcher Node
        Node(
            package="ros2_laser_scan_matcher",
            executable="laser_scan_matcher",
            name="laser_scan_matcher_node",
            parameters=[{
                'use_imu' : True,
                'use_odom' : True,
                "publish_tf": False,
                'kf_dist_linear': 0.10,
                'kf_dist_angular': 0.17,
                "publish_odom": "/laser_odom",
                "laser_frame": "lidar_link",
                "max_iterations": 10,
                'use_sim_time': LaunchConfiguration('use_sim_time'),
            }],
            remappings=[('/odom', '/odom_pub'), ('/imu/data', '/imu_pub')]

        ),
        
        # EKF Node passing the absolute path to the YAML file
        Node(
            package="robot_localization",
            executable="ekf_node",
            name="ekf_filter_node",
            parameters=[ekf_config_path,
                       {'use_sim_time': LaunchConfiguration('use_sim_time')},]
        ),

        # ExecuteProcess(
        #     cmd = [
        #         "ros2", "bag", "record", "-o", "data", "/imu_pub", "/odom_pub", "/odometry/filtered"
        #     ]
        # )
    ])