from setuptools import setup, find_packages

setup(
    name='univ360',
    version='0.1.6',
    author='Anton Zhidkov, Vlad Bespalov',
    packages=['univ360'],
    description='Module for v360 files',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.10',
    install_requires=[
        'urllib3',
        'Pillow',
    ],
)
