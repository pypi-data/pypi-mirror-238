from setuptools import setup, find_packages

VERSION = '1.0.4' 
DESCRIPTION = 'Leostream Python client'
LONG_DESCRIPTION = 'Leostream REST API client written in Python'

# Setting up
setup(
        name="leostream", 
        version=VERSION,
        author="Joost Evertse",
        author_email="<joustie@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], 
        keywords=['python', 'leostream', 'rest', 'api', 'client'],
        classifiers= [
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "Environment :: Console",
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
        ]
)
