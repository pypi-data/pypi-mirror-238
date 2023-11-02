
from setuptools import setup, find_packages

readme = open("./README.md","r")

setup(
    name='connectorcomet',
    version='0.1',
    packages=['connectorcomet'],
    install_requires=[
        'pandas',
        'requests'
    ],
    author='Lucas Bracamonte',
    author_email='ing.lucasbracamonte@gmail.com',
    description='A Python package to connect to the Comet API',
    long_description=readme.read(),
    long_description_content_type='text/markdown',
    #url='https://github.com/yourusername/cometconnector',  # Optional: your repository URL
)

