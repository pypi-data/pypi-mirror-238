from setuptools import setup, find_packages

setup(
    name='web3checksum',
    version='0.1.1',
    author='WebDev',
    author_email='webdev181011@gmail.com',
    description='Checksum of web3 address',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)