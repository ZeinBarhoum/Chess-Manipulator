import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

import xacro


def generate_launch_description():

    pkg_name = 'chess_manipulator' #the package name
    
    pkg_share= get_package_share_directory(pkg_name)
    
    urdf_path = 'description/manipulator.gazebo.urdf.xacro'

    rviz_relative_path= 'rviz/config.rviz'

    rviz_absolute_path = os.path.join(pkg_share, rviz_relative_path)
    
    # extracting the robot deffinition from the xacro file
    xacro_file = os.path.join(pkg_share, urdf_path)
    robot_description_content = xacro.process_file(xacro_file).toxml()

    # robot state publisher node
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description_content}]
    )
    # Rviz2 node
    node_rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments= ['-d', rviz_absolute_path]
    )
    # Gazebo launch file
    launch_gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('gazebo_ros'), 'launch'), '/gazebo.launch.py']),
    )
    # entity spawn node (to spawn the robot from the /robot_description topic)
    node_spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'my_bot'],
                        output='screen')
    
    # Run the nodes
    return LaunchDescription([
        node_robot_state_publisher,
        launch_gazebo,
        node_spawn_entity,
        node_rviz,
    ])
