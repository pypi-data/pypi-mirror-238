from setuptools import setup, find_packages

VERSION = '0.0.4' 
DESCRIPTION = 'Tarski\'s World for python'
LONG_DESCRIPTION = 'A python version of the Tarski\'s World universe'

# Setting up
setup(
       # the name must match the folder name 'pytarski'
        name="pytarski",
        version=VERSION,
        author="Walt Jacob",
        author_email="jacobw56@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'pytarski'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Environment :: Console",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: POSIX :: Linux",
        ]
)