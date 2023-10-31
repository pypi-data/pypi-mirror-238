from setuptools import find_packages, setup

setup(
    name="reach_commons",
    version="0.4.0",
    packages=find_packages(),
    install_requires=[],
    author="Wilson Moraes",
    author_email="wmoraes@getreach.ai",
    description="Uma descrição curta da sua biblioteca",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
