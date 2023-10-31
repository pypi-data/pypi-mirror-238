import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="alal",
    version="1.0.0",
    description="Python SDk for Alal's API",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ALAL-Community/alal-python",
    author="Alal",
    author_email="info@saalal.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    install_requires=["requests"],
    packages=find_packages(),
    python_requires=">=3.6"
)
