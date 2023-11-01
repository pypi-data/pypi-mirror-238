from setuptools import setup, find_packages

VERSION = '0.0.9' 
DESCRIPTION = 'A Package that includes utility functions'
LONG_DESCRIPTION = 'utils package that includes multiple utility functions that are used in different projects'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="SoiUtils", 
        version=VERSION,
        author="Sharon Komissarov",
        author_email="sharon200102@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['numpy','opencv-python','torch'], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3"
        ]
)