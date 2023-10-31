from setuptools import find_packages, setup

setup(
    name="dicttowddx",
    packages=find_packages(include=["dicttowddx"]),
    version="0.1.1",
    description="Use this utility lib to convert python dictionaries to valid WDDX data exchange "
    "format",
    author="Oyedotun Oyesanmi",
    author_email="dotunoyesanmi@gmail.com",
    url="https://github.com/dotman14/dicttowddx",
    install_requires=["yattag"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest==7.4.3"],
    test_suite="tests",
)
