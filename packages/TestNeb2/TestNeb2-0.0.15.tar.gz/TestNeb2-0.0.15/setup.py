from setuptools import setup

setup(
    name='TestNeb2',
    version='0.0.15',    
    description='An Engine For Building 2d Games With Python+Pygame-CE.',
    url='https://github.com/setoyuma/NebulaEngine',
    author='Setoichi',
    author_email='setoichi.dev@gmail.com',
    license='MIT',
    packages=['Nebula'],
    install_requires=[
        'pygame-ce',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha'
    ],
    package_data={'TestNeb2' : ['Nebula/templates']}
)