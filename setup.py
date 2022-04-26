import os

from setuptools import find_packages, setup

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

README = open(os.path.join(SCRIPT_DIR, "README.md")).read()

setup(
    name="qd",
    version="0.0.0a1",
    description="quickdraw - a cli plotting tool",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/velicanu/qd",
    author="Dragos Velicanu",
    author_email="qd@velicanu.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
    packages=find_packages(where="src"),
    include_package_data=True,
    install_requires=[
        "click==8.1.2",
        "imgcat==0.5.0",
        "kaleido==0.2.1",
        "numpy==1.22.3",
        "pandas==1.4.2",
        "plotly==5.7.0",
        "python-dateutil==2.8.2",
        "pytz==2022.1",
        "six==1.16.0",
        "tenacity==8.0.1",
    ],
    entry_points={
        "console_scripts": [
            "black=qd:main",
        ]
    },
)
