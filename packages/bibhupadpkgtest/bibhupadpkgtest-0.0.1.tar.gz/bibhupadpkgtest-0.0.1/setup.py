import setuptools

setuptools.setup(
    include_package_data=True,
    name='bibhupadpkgtest',
    version='0.0.1',
    description='ADI python package module',
    url='https://github.com/bibhupadt/MyDemoPackage',
    author='Bibhupad',
    author_email='bibhupad@gmail.com',
    packages=setuptools.find_packages(),
    long_description='bibhupad python module',
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
         "Operating System :: OS Independent",
    ],
)