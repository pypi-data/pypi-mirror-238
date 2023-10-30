from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="first-package-andrey-vorobyov",
    version="0.0.3",
    description="my first package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=find_packages("src",
                           include=["first_package_andrey_vorobyov*"]),
    author="Andrey Vorobyov",
    author_email="andrey.vorobyov@mail.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # install_requires=["bson >= 0.5.10"],
    # extras_require={
    #    "dev": ["pytest>=7.0", "twine>=4.0.2"],
    # },
    python_requires=">=3.10",
)