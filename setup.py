from setuptools import find_packages
#from setuptools import setup
from distutils.core import setup

with open('README.rst') as file:
    long_description = file.read()

setup(name='noaa-sdk',
      version='0.1.0',
      description='NOAA Python SDK',
      install_requires=[
          'httplib2==0.10.3',
          'urllib3==1.22'
      ],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.4'
      ],
      keywords='noaa weather public v3 api sdk',
      url='https://github.com/paulokuong/noaa',
      author='Paulo Kuong',
      author_email='paulo.kuong@gmail.com',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      long_description=long_description)
