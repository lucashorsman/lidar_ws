# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, RegisterEventHandler
from launch.conditions import IfCondition
from launch.event_handlers import OnProcessExit
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution, LaunchConfiguration

from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # Declare arguments
    declared_arguments = []
    declared_arguments.append(
        DeclareLaunchArgument(
            "gui",
            default_value="true",
            description="Start RViz2 automatically with this launch file.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "use_mock_hardware",
            default_value="false",
            description="Start robot with mock hardware mirroring command to its states.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "use_sim_time",
            default_value="false",
            description="use simulation clock, set true if simulating w/gz"
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "use_keyboard_twist",
            default_value="false",
            description="publish cmd_vel from keyboard"
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "use_joy_twist",
            default_value="false",
            description="publish cmd vel from joystick"
        )
    )
    # Initialize Arguments
    gui = LaunchConfiguration("gui")
    use_mock_hardware = LaunchConfiguration("use_mock_hardware")
    use_sim_time = LaunchConfiguration("use_sim_time")
    use_keyboard_twist = LaunchConfiguration("use_keyboard_twist")
    use_joy_twist = LaunchConfiguration("use_joy_twist")

    # joy = LaunchConfiguration
    # Get URDF via xacro
    robot_description_content = Command(
        [
            PathJoinSubstitution([FindExecutable(name="xacro")]),
            " ",
            PathJoinSubstitution(
                [FindPackageShare("urg_node"), "urdf", "hokuyo_ust10.urdf.xacro"]
            ),
            " ",
            "use_mock_hardware:=",
            use_mock_hardware,
        ]
    )
    robot_description = {"robot_description": robot_description_content}


    rviz_config_file = PathJoinSubstitution(
        [FindPackageShare("iir_base"), "config", "iirbot_view.rviz"]
    )

    robot_state_pub_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="both",
        parameters=[robot_description,{'use_sim_time': use_sim_time}],
    )
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="log",
        arguments=["-d", rviz_config_file],
        parameters=[{'use_sim_time': use_sim_time}],
        condition=IfCondition(gui),
    )
    rf2o_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare("rf2o_laser_odometry"),
                "launch",
                "rf2o_laser_odometry.launch.py"
            ])
        )
    )


    #ros2 run urg_node urg_node_driver --ros-args --params-file launch/urg_node_ethernet.yaml
    urg_node = Node(
    package="urg_node",
    executable="urg_node_driver",
    name="urg_node_driver",
    output="screen",
    
)
    nodes = [    
        robot_state_pub_node,
        urg_node,
        rf2o_launch,
    ]

    return LaunchDescription(declared_arguments + nodes)
