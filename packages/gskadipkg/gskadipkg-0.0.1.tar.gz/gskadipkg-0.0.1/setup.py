import setuptools

setuptools.setup(
    include_package_data=True,
    name='gskadipkg',
    version='0.0.1',
    description='ADI python module',
    url='https://github.com/SaikiranGudla/mydemopackage',
    author='saikiran_g',
    author_email='saikiran5955@gmail.com',
    packages=setuptools.find_packages(),
    long_description='ADI python module',
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
         "Operating System :: OS Independent",
    ],
)