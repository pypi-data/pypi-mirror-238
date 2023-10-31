from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="dicttowddx",
    packages=find_packages(include=["dicttowddx"]),
    version="0.1.6",
    description="Utility lib to convert python dictionaries to valid WDDX data exchange "
    "format",
    author="Oyedotun Oyesanmi",
    long_description_content_type="text/markdown",
    author_email="dotunoyesanmi@gmail.com",
    url="https://github.com/dotman14/dicttowddx",
    install_requires=["yattag"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest==7.4.3"],
    test_suite="tests",
    python_requires=">=3.8.0",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
