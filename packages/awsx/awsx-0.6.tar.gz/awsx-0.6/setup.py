from setuptools import setup

setup(
    name='awsx',
    version='0.6',
    py_modules=['main'],
    install_requires=[
        'Click',
        'boto3'
    ],
    entry_points='''
        [console_scripts]
        awsx=main:role_token
    ''',
)