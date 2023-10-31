import setuptools

setuptools.setup(
    include_package_data=True,
    name='csadipkg',
    version='0.0.1',
    description='Chetan ADI python Package module',
    url='https://github.com/csuresh/mydemopackage/myadipkg',
    author='chetanms',
    author_email='chetan4ms@gmail.com',
    packages=setuptools.find_packages(),
    long_description='Chetan ADI python Package module',
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
         "Operating System :: OS Independent",
    ],
)