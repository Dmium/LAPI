from setuptools import setup

setup(
    name='lazyAPI',
    packages=['lazyAPI',
              'lazyAPI.controllers',
              'lazyAPI.models'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-pymongo',
        'flask-login',
        'flask-bcrypt',
        'flask-wtf',
        'flask-talisman'
    ],
)
