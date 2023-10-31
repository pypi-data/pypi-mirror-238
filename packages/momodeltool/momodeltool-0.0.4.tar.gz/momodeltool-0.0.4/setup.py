import setuptools

with open("README.md",'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name = "momodeltool",
    version = "0.0.4",
    author = "momodeltool",
    author_email = "jianqi.sun@metoak.net",
    description = "This is a demo.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url="https://github.com/",
    packages=setuptools.find_packages(),
    install_requires=['opencv-python','numpy','torch'],
    # add any additional packages that needs to be installed along with SSAP package. 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)