import setuptools

setuptools.setup(
    include_package_data=True,
    name='hksadipkg',
    version='0.0.1',
    description='ADI python Package module',
    url='https://github.com/hkshitesh/mydemopackage',
    author='hiteshupes',
    author_email='hiteshupes@gmail.com',
    packages=setuptools.find_packages(),
    long_description='ADI python Package module',
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
         "Operating System :: OS Independent",
    ],
)