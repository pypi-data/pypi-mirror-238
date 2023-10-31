import setuptools

setuptools.setup(
    include_package_data=True,
    name='myadicalcpkg',
    version='0.0.1',
    description='ADI Python Package Module',
    url='https://github.com/vasu819/mydemopackage',
    author='vschennu',
    author_email='vschennu@gmail.com',
    packages=setuptools.find_packages(),
    long_description='ADI Python Package Module',
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
         "Operating System :: OS Independent",
    ],
)
