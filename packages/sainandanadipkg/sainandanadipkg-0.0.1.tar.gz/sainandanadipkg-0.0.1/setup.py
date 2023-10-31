import setuptools

setuptools.setup(
    include_package_data=True,
    name='sainandanadipkg',
    version='0.0.1',
    description='ADI Python Package Calculator module',
    url='https://github.com/SainandanD/mydemopackage',
    author='sainandan',
    author_email='nandansaid@gmail.com',
    packages=setuptools.find_packages(),    
    long_description='ADI Python calculator module',
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
         "Operating System :: OS Independent",
    ],
)