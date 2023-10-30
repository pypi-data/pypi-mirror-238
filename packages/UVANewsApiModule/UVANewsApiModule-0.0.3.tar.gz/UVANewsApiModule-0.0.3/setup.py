from setuptools import setup, find_packages

VERSION = '0.0.3' 
DESCRIPTION = "API for news from the University of Virginia's website"
LONG_DESCRIPTION = "API for news from the University of Virginia's website"

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="UVANewsApiModule", 
        version=VERSION,
        author="Benjamin Pusch",
        author_email="benjaminpusch03@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['asyncio','aiohttp','requests','datetime'],
        
        keywords=['python',],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)