from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

extras_requirements = {
    "test": [
        "pytest",
        "coverage",
    ],
}

setup(
    name="khmerencoding",
    version="0.1.1",
    description="Khmer character encoding based on the [khmer character specification](https://github.com/sillsdev/khmer-character-specification).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/maohieng/khmerencoding",
    author="Hieng MAO",
    author_email="maohieng@gmail.com",
    license="Apache License 2.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Natural Language :: English",
    ],
    packages=find_packages(),
    install_requires=[],
    include_package_data=True,
    python_requires='>=3.5'
)