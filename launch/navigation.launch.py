import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription
from launch_ros.actions import Node
from launch.actions import TimerAction

def generate_launch_description():
    package_name = 'diff_drive_robot'
    configuration_directory = os.path.join(
        get_package_share_directory(package_name), 'config')
    map_file = os.path.join(configuration_directory, 'map.yaml')

    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(
                get_package_share_directory('diff_drive_robot'), 'launch', 'robot.launch.py'
            )]),
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(
                get_package_share_directory('nav2_bringup'), 'launch', 'bringup_launch.py'
            )]),
            launch_arguments={
                'map': map_file,
                'use_sim_time': 'true',
                'params_file': os.path.join(configuration_directory, 'nav2_params.yaml'),
                'autostart': 'true'
            }.items()
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', os.path.join(get_package_share_directory('diff_drive_robot'), 'config', 'navigation.rviz')],
            parameters=[{'use_sim_time': True}]
        ),
    ])
