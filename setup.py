import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pythonmq",
    version="1.0.0",
    author="Carlos Armando",
    author_email="contato.carmando@gmail.com",
    description="Pure Python 3 implementation of local messageque IPC",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/InfeCtlll3/pythonmq",
    license="BSD",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
    ],
)