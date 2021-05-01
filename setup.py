from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='video',
    version='0.0.1',
    description='for sending opencv video from socket ',
    author='Umang Shrestha',
    author_email='umangshrestha09@gmail.com',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=required,
    python_requires='>=3.8',
)