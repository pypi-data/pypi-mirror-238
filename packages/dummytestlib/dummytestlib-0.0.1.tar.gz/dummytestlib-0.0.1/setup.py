from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'A dummy test package'
LONG_DESCRIPTION = 'A package not intended for use by anyone.'

setup(
    name="dummytestlib",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Me",
    author_email="dummytestpackage@dummytest.com",
    license='MIT',
    packages=find_packages(include=["dummytestlib"]),
    install_requires=[],
    keywords='conversion',
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
    ]
)