from setuptools import setup, find_packages  
  
setup(  
    name='GreSec',  
    version='0.1',  
    packages=find_packages(),  
    description='A package for checking suspicious contracts',  
    author='AkashGreninja',  
    author_email='akashuhulekal@gmail.com',  
    install_requires=[  
        'fastapi',  
        'python-dotenv',  
        'pymongo',  
        'requests',  
        'bs4'  
    ],  
)  
