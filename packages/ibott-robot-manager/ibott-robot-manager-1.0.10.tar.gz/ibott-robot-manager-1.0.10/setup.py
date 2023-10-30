from setuptools import setup, find_packages

setup(
    name="ibott-robot-manager",
    version="1.0.10",
    packages=find_packages(),
    install_requires=["hatchling", "requests", "python-decouple==3.1"],
    author="OnameDohe",
    author_email="enrique.crespo.debenito@gmail.com",
    description="This packages allows to use ibott robot console features.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ecrespo66/robot-manager",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
