from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='spacetrack_files',
  version='0.0.3',
  author='Flexlug',
  author_email='flexlug@outlook.com',
  description='Simple module for ephemeris download and parse',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/Flexlug/spacetrack_files',
  packages=find_packages(),
  install_requires=[
    'requests>=2.31.0', 
    'pandas>=2.1.2', 
    'tqdm>=4.66.1', 
    'numpy>=1.26.1'
  ],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='spacetrack ephemeris starlink',
  project_urls={
    'GitHub': 'https://github.com/Flexlug'
  },
  python_requires='>=3.7'
)
