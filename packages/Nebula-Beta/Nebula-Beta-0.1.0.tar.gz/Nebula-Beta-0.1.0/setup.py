from setuptools import setup

setup(
    name='Nebula-Beta',
    version='0.1.0',
    description='An Engine For Crafting 2d Games With Python+Pygame-Ce.',
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
        'Development Status :: 4 - Beta'
    ],
)