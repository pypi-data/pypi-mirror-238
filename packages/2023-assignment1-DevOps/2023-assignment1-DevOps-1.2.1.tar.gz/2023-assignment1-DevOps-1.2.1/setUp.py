from setuptools import setup, find_packages

setup(
    name='2023-assignment1-DevOps',
    version='1.2.1',
    description='Assignment1',
    author='GruppoELA',
    author_email='l.perfetti2001@gmail.com',
    packages=find_packages(),
    install_requires=[
        'pymongo',
        'pytest', 
        'prospector',
        'bandit',
        'mkdocs',
    ],
)
