from setuptools import setup, find_packages

setup(
    name='dislord',
    version='0.0.1',
    author='Jack Draper',
    author_email='drapj002@gmail.com',
    description='A serverless optimized discord API library using interactions.',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)