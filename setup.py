import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "centaurminer",
    version = "0.0.2",
    author = "Simon Ewing",
    author_email = "Simonsays095@gmail.com",
    description = "A selenium wrapper to help mining data from scientific literature.",
    long_description = long_description,
    long_description_content_type = "text/x-rst",
    url = "https://github.com/Simonsays095/CENTAURminer.git",
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
    ],
    python_requires = '>=3.4',
    install_requires = [
        'selenium',
        'webdriver_manager'
    ],
    project_urls = {
        'Documentation': 'https://centaurminer.readthedocs.io/',
        'Source code': 'https://github.com/Simonsays095/CENTAURminer'
    }
)
