from os import path

from setuptools import setup

HERE = path.abspath(path.dirname(__file__))
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
setup(
    name='dynai',
    version='0.1.0',
    packages=['dynai'],
    url='https://dynai.readthedocs.io/',
    license='MIT License',
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    author='Arian Ott',
    author_email='learning.ott@gmail.com',
    description='Dynamic AI',
    include_package_data=True,
    long_description=long_description,
    long_description_content_type='text/markdown'
)
