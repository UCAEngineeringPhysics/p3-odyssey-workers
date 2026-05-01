from setuptools import find_packages, setup
import os
from glob import glob
from pathlib import Path

package_name = 'coffee_car'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        
        # FIXED: Destination directory, followed by a list of source files
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
        
        # FIXED: Same tuple structure for the launch folder
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),

         (
            str(Path("share") / package_name / "rviz"),
            [str(p) for p in Path("rviz").glob("*.rviz")],
        ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='worker',
    maintainer_email='phillips85502@gmail.com',
    description='Autonomous coffee delivery robot',
    license='MIT',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'pico_interface = coffee_car.pico_interface:main',
            'action = coffee_car.action:main',
        ],
    },
)
