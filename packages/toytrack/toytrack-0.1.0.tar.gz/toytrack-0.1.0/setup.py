from setuptools import setup, find_packages

setup(
    name='toytrack',
    version='0.1.0',
    url='https://github.com/murnanedaniel/toytrack',
    author='Author Name',
    author_email='author@gmail.com',
    description='Description of my package',
    packages=find_packages(),    
    install_requires=['numpy >= 1.11.1', 'pandas >= 0.18.1'],
)