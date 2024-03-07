# 导入库
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    """launch内容描述函数，由ros2 launch 扫描调用"""
    ldlidar_node = Node(
      package='ldlidar_sl_ros2',
      executable='ldlidar_sl_ros2_node',
      name='ldlidar_publisher_ld14',
      output='screen',
      parameters=[
        {'product_name': 'LDLiDAR_LD14'},
        {'laser_scan_topic_name': 'scan'},
        {'point_cloud_2d_topic_name': 'pointcloud2d'},
        {'frame_id': 'base_laser'},
        {'port_name': '/dev/ttyUSB0'},
        {'serial_baudrate' : 115200},
        {'laser_scan_dir': True},
        {'enable_angle_crop_func': False},
        {'angle_crop_min': 135.0},
        {'angle_crop_max': 225.0}
      ]
    )
    
#    imu_node = Node(
#        package="imu_package",
#        executable="run_imu"
#    )
    
    controller_node = Node(
        package="car_controller",
        executable="run_controller"
    )
    
    # 创建LaunchDescription对象launch_description,用于描述launch文件
    launch_description = LaunchDescription(
        [
            ldlidar_node, 
            #imu_node, 
            controller_node
        ])
    # 返回让ROS2根据launch描述执行节点
    return launch_description

