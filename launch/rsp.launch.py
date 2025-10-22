from launch_ros.actions import Node
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, Command
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
    pkg_share = FindPackageShare("diff_drive_robot")

    # Arguments
    prefix_arg = DeclareLaunchArgument(
        'prefix', default_value='robot_1',
        description='Prefix for robot instance name')
    
    x_arg = DeclareLaunchArgument('x', default_value='0.0')
    y_arg = DeclareLaunchArgument('y', default_value='0.0')
    z_arg = DeclareLaunchArgument('z', default_value='0.1')

    prefix = LaunchConfiguration('prefix')
    x = LaunchConfiguration('x')
    y = LaunchConfiguration('y')
    z = LaunchConfiguration('z')

    # Proper Xacro expansion with parameters
    robot_description = Command([
        'xacro ', 
        PathJoinSubstitution([
            FindPackageShare('diff_drive_robot'),
            'urdf',
            'robot.xacro'
        ]),
        ' prefix:=', prefix
    ])

    # Robot State Publisher node
    rsp_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',  # Don't prefix this name
        namespace=prefix,  # Use namespace instead of name prefix
        output='screen',
        parameters=[{
            'use_sim_time': True, 
            'robot_description': ParameterValue(robot_description, value_type=str)
        }]
    )

    # Spawn in Gazebo
    spawn_node = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-topic', ['/', prefix, '/robot_description'],  # Use namespaced topic
            '-name', prefix,
            '-x', x,
            '-y', y,
            '-z', z
        ],
        output='screen'
    )

    return LaunchDescription([
        prefix_arg,
        x_arg,
        y_arg,
        z_arg,
        rsp_node,
        spawn_node
    ])