
from setuptools import setup, find_packages

setup(
    name='comet-connector',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'requests'
    ],
    author='Lucas Bracamonte',
    description='A Python package to connect to the Comet API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/comet-connector',  # Optional: your repository URL
)

