from setuptools import setup

package_name = 'vernie_controller'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='niels',
    maintainer_email='niels.hygum.nielsen@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': ['vernie_control = vernie_controller.vernie_controll:main','vernie_main = vernie_controller.vernie_main:main'],
    },
)
