from setuptools import setup

setup(
    name='lazyAPI',
    packages=['lazyAPI',
              'lazyAPI.controllers'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-pymongo'
    ],
)
