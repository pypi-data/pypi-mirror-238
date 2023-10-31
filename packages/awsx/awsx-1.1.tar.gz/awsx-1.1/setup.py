from setuptools import setup

setup(
    name='awsx',
    version='1.1',
    py_modules=['main'],
    install_requires=[
        'Click',
        'boto3',
        'configparser',
        'pyperclip',
    ],
    entry_points='''
        [console_scripts]
        awsx=main:role_token
    ''',
)