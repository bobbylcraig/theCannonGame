from setuptools import setup

setup(
    name='The Cannon Game',
    version='1.0',
    author='Bobby Craig',
    py_modules=['spam_sam'],
    install_requires=['math', 'urllib.requests', 'time', 'random'],
    entry_points='''
        [console_scripts]
        CannonGameCode=CannonGameCode:main
    ''',
)