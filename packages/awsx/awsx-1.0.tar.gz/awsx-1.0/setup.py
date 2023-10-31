from setuptools import setup

setup(
    name='awsx',
    version='1.0',
    py_modules=['main'],
    install_requires=[
        'Click',
        'boto3',
        'configparser',
        'pyperclip',
        'platform',
        'os'
    ],
    entry_points='''
        [console_scripts]
        awsx=main:role_token
    ''',
)