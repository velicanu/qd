import os

from setuptools import find_packages, setup

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

README = open(os.path.join(SCRIPT_DIR, "README.md")).read()

setup(
    name="qd-plot",
    version="0.0.3",
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
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=["click", "imgcat", "kaleido", "pandas", "plotly"],
    entry_points={
        "console_scripts": [
            "qd=qd:main",
        ]
    },
)
