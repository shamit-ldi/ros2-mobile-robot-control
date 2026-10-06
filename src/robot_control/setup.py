from setuptools import find_packages, setup

package_name = 'robot_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name],
        ),
        (
            'share/' + package_name,
            ['package.xml'],
        ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='shamitk3107',
    maintainer_email='shamitk3107@todo.todo',
    description='ROS 2 mobile robot control package',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'velocity_publisher = robot_control.velocity_publisher:main',
            'odometry_subscriber = robot_control.odometry_subscriber:main',
            'point_controller = robot_control.point_controller:main',
        ],
    },
)
