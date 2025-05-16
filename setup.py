# setup.py

from setuptools import setup, find_packages

setup(
    name="proofai",
    version="0.1.0",
    description="Stub SDK for Agent Hub agent development",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Osadebe Chijioke Akaolisa",
    author_email="osadebec98@email.com",
    url="https://github.com/CijeTheCreator/proofai",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
    ],
    entry_points={
        'console_scripts': [
            'proofai=proofai.cli:main',
        ],
    },
)
