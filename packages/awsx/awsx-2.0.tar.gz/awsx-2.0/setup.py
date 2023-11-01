from setuptools import setup

setup(
    name='awsx',
    version='2.0',
    py_modules=['main'],
    install_requires=[
        'Click',
        'boto3',
        'configparser',
        'pyperclip',
        'psutil'
    ],
    entry_points='''
        [console_scripts]
        awsx=main:role_token
    ''',
)