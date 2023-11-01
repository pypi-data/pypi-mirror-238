from setuptools import setup, find_packages

def read_requirements():
    with open('requirements.txt', 'r') as file:
        return [line.strip() for line in file.readlines()]

setup(
    name="cellplot",
    version="0.3",
    packages=find_packages(),
    install_requires=read_requirements(),
    author="Your Name",
    author_email="your.email@example.com",
    description="A brief description of your package",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/SimonBon/cellplot",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
)
