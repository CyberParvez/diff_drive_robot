import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    pkg = get_package_share_directory('diff_drive_robot')

    world = LaunchConfiguration('world')
    rviz = LaunchConfiguration('rviz')

    world_path = os.path.join(pkg, 'worlds', 'obstacles.world')
    declare_world = DeclareLaunchArgument('world', default_value=world_path)
    declare_rviz = DeclareLaunchArgument('rviz', default_value='True')

    # Gazebo sim
    # Launch the gazebo server to initialize the simulation
    gazebo_server = IncludeLaunchDescription(
                    PythonLaunchDescriptionSource([os.path.join(
                        get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py'
                    )]), launch_arguments={'gz_args': ['-r -s -v1 ', world], 'on_exit_shutdown': 'true'}.items()
    )

    # Always launch the gazebo client to visualize the simulation
    gazebo_client = IncludeLaunchDescription(
                    PythonLaunchDescriptionSource([os.path.join(
                        get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py'
                    )]), launch_arguments={'gz_args': '-g '}.items()
    )
    
    # Spawn Robot 1
    robot1 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(pkg, 'launch', 'rsp.launch.py')]),
        launch_arguments={
            'prefix': 'robot_1',
            'x': '0',
            'y': '0'
        }.items()
    )

    # Spawn Robot 2
    robot2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(pkg, 'launch', 'rsp.launch.py')]),
        launch_arguments={
            'prefix': 'robot_2',
            'x': '1',
            'y': '0'
        }.items()
    )

    # Gazebo-ROS bridge
    bridge_params = os.path.join(pkg, 'config', 'gz_bridge.yaml')
    ros_gz_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[
            '--ros-args', '-p', f'config_file:={bridge_params}'
        ]
    )

    rviz_node= Node(
        condition=IfCondition(rviz),
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', os.path.join(pkg, 'rviz', 'bot.rviz')],
        output='screen'
    )

    return LaunchDescription([
        declare_world,
        declare_rviz,
        gazebo_server,
        gazebo_client,
        robot1,
        robot2,
        rviz_node,
        ros_gz_bridge
    ])
