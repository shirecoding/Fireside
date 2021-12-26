from distutils.core import setup

from setuptools import find_packages

exec(open("fsg_agent/version.py").read())
setup(
    name="fsg_agent",
    version=__version__,
    author="shirecoding",
    author_email="shirecoding@gmail.com",
    install_requires=["powerful-agents", "requests"],
    extras_require={},
    scripts=["bin/fsg_agent"],
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
