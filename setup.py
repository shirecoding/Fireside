from distutils.core import setup
from setuptools import find_packages
from fireside import __version__

setup(
    name="fireside",
    version=__version__,
    author="",
    author_email="",
    install_requires=["PyFiglet", "clint", "rxpipes", "powerful-agents"],
    scripts=["bin/fireside"],
    url="https://github.com/shirecoding/Fireside.git",
    download_url=f"https://github.com/shirecoding/Fireside/archive/{__version__}.tar.gz",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    zip_safe=False,
    include_package_data=True,
    packages=find_packages() + [],
    package_data={},
)
