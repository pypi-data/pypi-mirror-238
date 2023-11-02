# /setup.py
import os
import setuptools
import package_profile


with open("README.md", "r") as fh:
    long_description = fh.read()


def get_requirements():
    """
    Return a list of required packages in requirements
    """
    os.path.join(os.path.dirname(__file__), "requirements.txt")
    with open(os.path.join(os.path.dirname(__file__), "requirements.txt")) as f:
        return [
            i for i in f.read().splitlines() if i.strip() != "" and "#" != i.strip()[0]
        ]


setuptools.setup(
    name=package_profile.package_name,
    version=package_profile.version,
    author=package_profile.authors,
    author_email=package_profile.author_email,
    description=package_profile.description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=package_profile.url,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=get_requirements(),
    include_package_data=True,
)
