from setuptools import find_packages
from distutils.core import setup

with open('README.rst') as file:
    long_description = file.read()

setup(name='noaa-sdk',
      version='0.1.20',
      description='NOAA API (V3) Python 3 SDK.',
      install_requires=[
          'requests>=2.22.0'
      ],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.4'
      ],
      keywords=(
          'NOAA noaa weather public v3 api sdk osm postalcode country postcode'),
      url='https://github.com/paulokuong/noaa',
      author='Paulo Kuong',
      author_email='paulo.kuong@gmail.com',
      license='MIT',
      packages=find_packages(exclude=["tests"]),
      include_package_data=True,
      zip_safe=False,
      long_description=long_description)
