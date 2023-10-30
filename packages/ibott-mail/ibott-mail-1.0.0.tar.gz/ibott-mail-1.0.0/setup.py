from setuptools import setup, find_packages

setup(
    name="ibott-files",
    version="1.0.5",
    packages=find_packages(),
    install_requires=["hatchling", "imap-tools==0.16.1"],
    author="OnameDohe",
    author_email="enrique.crespo.debenito@gmail.com",
    description="This packages crates a simple way to work with, emails, send, read and download attachments",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ecrespo66/files_and_folders",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
