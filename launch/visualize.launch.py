"""
@file visualize.launch.py
@brief
    Launch file for visualizing Magnet URDF
@author
    Tobit Flatscher <tobit@robots.ox.ac.uk>
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import AndSubstitution, LaunchConfiguration, NotSubstitution
from launch_ros.actions import Node


def generate_launch_description():
    simulation_parameter_name = 'simulation'
    simulation = LaunchConfiguration(simulation_parameter_name)

    #gazebo_ign_parameter_name = 'gazebo_ign'
    #gazebo_ign = LaunchConfiguration(gazebo_ign_parameter_name)

    simulation_parameter_arg = DeclareLaunchArgument(
        simulation_parameter_name,
        default_value='true',
        description='Simulated or real hardware interface'
    )

    #gazebo_ign_arg = DeclareLaunchArgument(
    #    gazebo_ign_parameter_name,
    #    default_value='true',
    #    description='Use Gazebo Ignition or alternatively Gazebo Classic'
    #)

    description_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(
                    get_package_share_directory('magnet_description'),
                    'launch', 'description.launch.py'
                )
            ]
        ),
        launch_arguments={
            'simulation': simulation
        }.items()
    )

    rviz_file = os.path.join(
        get_package_share_directory('magnet_description'),
        'rviz',
        'model.rviz'
    )
    rviz_node = Node(package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['--display-config', rviz_file]
    )

    #is_gazebo_ign = AndSubstitution(simulation, gazebo_ign)
    #is_gazebo_classic = AndSubstitution(simulation, NotSubstitution(gazebo_ign))

    # Gazebo Ignition (recommended)
    """
    gazebo_ign_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(
                    get_package_share_directory('ros_gz_sim'),
                    'launch', 'gz_sim.launch.py'
                )
            ]
        ),
        launch_arguments={
            'gz_args': " -r -v 3 empty.sdf"
        }.items(),
        condition=IfCondition(is_gazebo_ign)
    )
    gazebo_ign_spawner_node = Node(
        package="ros_gz_sim",
        executable="create",
        output="screen",
        arguments=[
            "-topic",
            "/robot_description",
            "-name",
            "magnet",
            "-allow_renaming",
            "true",
        ]
    )
    """
    
    # Gazebo Classic (deprecated)
    gazebo_classic_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(
                    get_package_share_directory('gazebo_ros'),
                    'launch', 'gazebo.launch.py'
                )
            ]
        ),
        condition=IfCondition(simulation)
    )
    gazebo_classic_spawner_node = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='gazebo_spawner',
        arguments=['-entity', 'magnet', '-topic', 'robot_description'],
        output='screen',
        condition=IfCondition(simulation)
    )

    ld = LaunchDescription()
    ld.add_action(simulation_parameter_arg)
    #ld.add_action(gazebo_ign_arg)
    ld.add_action(description_launch)
    ld.add_action(rviz_node)
    #ld.add_action(gazebo_ign_node)
    #ld.add_action(gazebo_ign_spawner_node)
    ld.add_action(gazebo_classic_node)
    ld.add_action(gazebo_classic_spawner_node)
    return ld