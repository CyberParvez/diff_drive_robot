import os 
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    configuration_directory = os.path.join(
        get_package_share_directory('diff_drive_robot'), 'config')
    map_file = os.path.join(
        configuration_directory, 'map.yaml')
    return LaunchDescription([

        Node(
            package='cartographer_ros',
            executable='cartographer_node',
            name='cartographer_node',
            output='screen',
            arguments=[
                '-configuration_directory', configuration_directory,
                '-configuration_basename', 'cartographer.lua',
                # '--load_state_filename', map_file
            ]),
        Node(
            package='cartographer_ros',
            executable='cartographer_occupancy_grid_node',
            name='cartographer_occupancy_grid_node',
            # arguments=[
            #     '-resolution', '0.05'
            # ],
            output='screen'
        ),
    ])