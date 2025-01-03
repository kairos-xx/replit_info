
from setuptools import setup, find_packages

setup(
    name="GitPyPi312",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        'requests',
        'replit',
        'toml'
    ],
    author="Joao Lopes",
    author_email="joaoslopes@gmail.com",
    description="",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kairos-xx/GitPyPi312",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)
