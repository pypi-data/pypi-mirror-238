from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")


setup(
    name="dataos-pyflare",

    version="0.0.7",

    description="Pyspark bridge to dataos",

    long_description=long_description,

    long_description_content_type="text/markdown",

    url="https://bitbucket.org/rubik_/dataos-pyspark-sdk",

    author="Modern labs",
    author_email="labs@tmdc.io",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Customer Service",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
    ],

    keywords="dataos, python flare, pyflare, dataos-pyflare",


    package_dir={
        "pyflare": "pyflare",
    },


    # packages=find_packages(),
    packages=['pyflare', 'pyflare.secrets', 'pyflare.sdk', 'pyflare.jars',
              'pyflare.sdk.config', 'pyflare.sdk.core', 'pyflare.sdk.depots',
              'pyflare.sdk.utils', 'pyflare.sdk.readers', 'pyflare.sdk.writers'],

    python_requires=">=3.7, <4",

    install_requires=["pyspark==3.3.1", "requests==2.31.0", "deprecation==2.1.0", "setuptools==68.0.0", "py4j==0.10.9.5"],

)
