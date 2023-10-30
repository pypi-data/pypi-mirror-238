import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "ninadTestPyPI",
    version = "0.1.5",
    author = "Ninad Rathod",
    author_email = "ninadrathod267@gmail.com",
    description = "A simple 'Hello, World!' package",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url="https://github.com/ninadrathod/ninad-test-run.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
