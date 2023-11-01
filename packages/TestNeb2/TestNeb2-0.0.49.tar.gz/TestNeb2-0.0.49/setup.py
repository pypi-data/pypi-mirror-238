from setuptools import setup

setup(
    name='TestNeb2',
    version='0.0.49',    
    description='An Engine For Building 2d Games With Python+Pygame-CE.',
    url='https://github.com/setoyuma/NebulaEngine',
    author='Setoichi',
    author_email='setoichi.dev@gmail.com',
    license='MIT',
    packages=['Nebula'],
    install_requires=[
        'pygame-ce',
        'pygame-gui'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha'
    ],
)