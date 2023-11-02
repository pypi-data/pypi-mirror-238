from setuptools import setup, find_packages

verSion = "0.0.3"

# with open("README.md", "r") as file:
#     descriptions = file.readlines()

_requires_packages = []
with open("requirements.txt", 'r') as rqfile:
    for pack in rqfile.readlines():
        _requires_packages.append(pack.replace('\n', ''))

setup(
    name="BioBeee",
    version=verSion,
    author="aniket_yadav",
    author_email="aniketyadav8687@gmail.com",
    packages=find_packages(),
    description="Bioinformatics tool for performing web scrapping on biological database and pre-processing",
    # long_description="Tool to analyze",
    # long_description_content_type="markdown",
    url="https://gitlab.com/aniket4033426/mini_project",
    license='MIT',
    python_requires='>=3.0',
    install_requires=_requires_packages
)