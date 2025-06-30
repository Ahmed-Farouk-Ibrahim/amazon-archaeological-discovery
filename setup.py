"""
Setup script for Amazon Archaeological Discovery System.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="amazon-archaeological-discovery",
    version="1.0.0",
    author="Ahmed Osman",
    author_email="engineer.ahmedfarouk@gmail.com",
    description="AI-powered archaeological site discovery in the Amazon using multi-sensor remote sensing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ahmed-Farouk-Ibrahim/amazon-archaeological-discovery.git",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: GIS",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "archaeological-discovery=scripts.run_discovery:main",
        ],
    },
)
