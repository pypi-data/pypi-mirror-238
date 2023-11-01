from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'Library created to map keys in dictionaries.'

# Setting up
setup(
    name="dictmaper",
    version=VERSION,
    author="Arnold Blandon and Santiago Gonzalez",
    author_email="arnold.blandon1@gmail.com",
    maintainer="Santiago Gonzalez",
    maintainer_email="alejandro980619@outlook.com",
    description=DESCRIPTION,
    long_description=open("README.rst").read(),
    long_description_content_type="text/x-rst",
    packages=find_packages(exclude=["tests"]),
    install_requires=[],
    keywords=['python', 'dict', 'map', 'data'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
