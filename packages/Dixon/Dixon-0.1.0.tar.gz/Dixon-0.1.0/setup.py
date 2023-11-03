from setuptools import setup, find_packages

setup(
    name='Dixon',
    version='0.1.0',
    author='Dixon MD',
    author_email='dixonmd@gmail.com',
    description='Print Dixon 10 times. Checking package in PyPi',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
