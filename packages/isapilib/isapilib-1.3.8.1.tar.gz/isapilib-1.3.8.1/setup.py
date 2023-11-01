from setuptools import setup, find_packages

setup(
    name='isapilib',
    version='1.3.8.1',
    packages=find_packages(),
    install_requires=[
        'django>=4.2',
        'djangorestframework>=3.0.0',
        'djangorestframework-simplejwt>=5.0.0',
    ],
)
