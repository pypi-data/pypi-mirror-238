from setuptools import setup
from setuptools import find_packages
setup(name='HPSM',
      version='0.0.1',
      description='',
      author='Xudong Yang',
      author_email='swithunyang@163.com',
      requires=['re','sys','numpy','torch','argparse','sklearn','decimal'],
      packages=find_packages(),
      license='apache 3.0'
)