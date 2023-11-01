import setuptools
 
with open("README.md", "r") as fh:
    long_description = fh.read()
 
setuptools.setup(
    name="dva_mlops_utils",
    version="0.0.1",
    author="DaVita MLOps",
    license="© 2023 DaVita Inc. All rights reserved.",
    author_email="MLOpsIntake&Support@davita.com",
    description="Python package for utility functions and other custom Python dependencies developed internally by the DaVita MLOps team.",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7'
)