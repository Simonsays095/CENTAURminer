import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="BREATHE-mining",
    version="0.0.1",
    author="Simon Ewing",
    author_email="Simonsays095@gmail.com",
    description="A selenium wrapper to help mining data for the BREATHE dataset.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
    ],
    python_requires='>=3.4',
)