from setuptools import setup, find_packages

setup(
    name="sqldao-generator",
    version="1.0.0",
    author="Daniel Hsu",
    description="SqlAlchemy DAO generator",
    long_description_content_type="text/markdown",
    url="https://github.com/davidhsusl/sqldao-generator",
    keywords="SQLAlchemy, mysql",
    python_requires=">=3.10, <4",
    py_modules=["sqldaogenerator"],  # Name of the python package
    package_dir={"": "."},  # Directory of the source code of the package
    packages=find_packages(include=["sqldaogenerator.*"]),
    package_data={"": ["*.json", "*.txt", "*.sql"]},
    install_requires=[
        "mysql-connector-python>=8.0.0,<9.0.0",
        "SQLAlchemy>=2.0.0,<3.0.0",
        "pandas>=2.0.1,<3.0.0"
    ],
    author_email="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
