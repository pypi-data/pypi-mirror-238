import os
from setuptools import setup, find_packages

base_dir = os.path.dirname(os.path.abspath(__file__))
docs_path = os.path.join(base_dir, 'docs.md')

setup(
    name='hanime',
    version='1.0.0',
    description='A simple Python wrapper for interacting with Hanime\'s API.',
    author='dancers.',
    author_email='bio@fbi.ac',
    url='https://github.com/lolpuud/hanime',
    packages=find_packages(include=['hanime*']),
    install_requires=[],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    long_description=open(docs_path).read(),
    long_description_content_type='text/markdown',
)
