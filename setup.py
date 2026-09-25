from setuptools import setup, find_packages

setup(
    name="rittiktool",
    version="1.6.0",
    packages=find_packages(),
    install_requires=[
        "rich",
    ],
    entry_points={
        "console_scripts": [
            "rittiktool=mitool.cli:main",
            "mitool=mitool.cli:main",
            "miflash=miflash.cli:main",
        ],
    },
)
