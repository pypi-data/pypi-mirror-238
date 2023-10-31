import setuptools

setuptools.setup(
    include_package_data=True,
    name='swaroopadipkg',
    version='0.0.1',
    description="Swaroop's Test Python Module",
    url='https://github.com/SwaroopPK/ADI-Modules',
    author='Swaroop',
    author_email='swarooppk96@gmail.com',
    packages=setuptools.find_packages(),
    long_description='ADI Python Package Module',
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
         "Operating System :: OS Independent",
    ],
)