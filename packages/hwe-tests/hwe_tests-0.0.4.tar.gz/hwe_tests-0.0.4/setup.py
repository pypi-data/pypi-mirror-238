import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hwe_tests",  # This is the name of the package
    version="0.0.4",  # The initial release version
    author="Or Shkuri",  # Full name of the author
    description="Chi Squared and Gibbs Sampling statistical tests for HWE",
    long_description=long_description,  # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),  # List of all python modules to be installed
    url="https://github.com/ExtraFlash/HWE_tests_package.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],  # Information to filter the project on PyPi website
    python_requires='>=3.6',  # Minimum version requirement of the package
    py_modules=["hwe_tests"],  # Name of the python package
    package_dir={'':'hwe_tests/src'},  # Directory of the source code of the package
    install_requires=[]  # Install other dependencies if any
)
