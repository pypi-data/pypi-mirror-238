from setuptools import setup, find_packages

setup(
    name="pytdv2",
    version="0.3",
    description="Official python library for trusted device from fazpass company",
    author="fazpass",
    license="MIT",
    author_email="info.fazpass@gmail.com",
    url="https://github.com/fazpass-sdk/python-trusted-device-v2",
    packages=find_packages(exclude=["tests*", "examples*"]),
    install_requires=[
        'pycryptodome'
    ],
    python_requires='>=3.4',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
