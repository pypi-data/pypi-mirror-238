import setuptools

setuptools.setup(
    include_package_data=True,
    name='somadipkg',
    version='0.0.1',
    description='ADI python package module',
    url='https://github.com/hkshitesh/mydemopackage',
    author='Somali',
    author_email='somalibhosale7@gmail.com',
    packages=setuptools.find_packages(),
    long_description='ADI python package module',
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
         "Operating System :: OS Independent",
    ],
)