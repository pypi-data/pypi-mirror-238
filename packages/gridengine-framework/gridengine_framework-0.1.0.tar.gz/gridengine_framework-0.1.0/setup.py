from setuptools import setup, find_packages

setup(
    name='gridengine_framework',
    version='0.1.0',
    description='A framework for generating and manipulating grid-based game worlds',
    author='James Evans',
    author_email='joesaysahoy@gmail.com',
    url='https://github.com/primal-coder/gridengine',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pillow',
        'pyglet',
        'pymunk'
    ],
    keywords='game development 2d grid world generation procedural generation cell numpy pillow pyglet pymunk cli'
)