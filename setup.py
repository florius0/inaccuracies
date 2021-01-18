from setuptools import setup

setup(
    name='inaccuracies',
    version='0.1.0',
    install_requires=[
        'pandas~=1.1.2',
        'setuptools~=47.1.0',
        'sympy~=1.6.2',
        'click~=7.1.2',
    ],
    entry_points={
        'console_scripts': ['inc = inaccuracies:main'],
    }
)
