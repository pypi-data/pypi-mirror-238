import setuptools
setuptools.setup(
    name = "Agently",
    version = "3.0.0-alpha-6",
    author = "Maplemx",
    author_email = "maplemx@gmail.com",
    description = "Agently, a framework to build applications based on language model powered intelligent agents.",
    long_description = "https://github.com/Maplemx/Agently",
    url = "https://github.com/Maplemx/Agently",
    packages = setuptools.find_packages(),
    package_data = {"": ["*.txt", "*.ini"]},
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)