from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="ocw_oer_export",
    version="0.1.0",
    author="",
    author_email="",
    description="A short description of your package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    readme="README.md",
    url="",
    project_urls={
        "X": "Y",
    },
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD 3-Clause License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
