from setuptools import setup, find_packages
setup(name='myColorfulLog',
    version='1.3.0',
    description='Colorful logger for terminal and log files. Based on previous work code by xyztank, https://www.cnblogs.com/xyztank/articles/13598633.html',
    author='brainix',
    author_email='brainix@buaa.edu.cn',
    requires= ['colorlog','logging'],
    install_requires=['colorlog'],
    packages=find_packages(),
    license="MIT"
)