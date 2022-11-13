"""Package setup."""

from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="confoid",
    description="Configuration Management for Python.",
    version="0.2.0",
    author="Savio Fernandes",
    author_email="savio@saviof.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/saviof-hub/confoid",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=["pyyaml==6.0"],
    extras_require={
        "dev": [
            'coverage[toml]',
            'pytest',
            'pytest-asyncio',
            'pytest-cov',
            'flake8',
            'flake8-docstrings',
            'black',
            'isort',
            'requests',
            'hypothesis',
            'mypy',
            'bandit',
            'pylint',
            "twine",
            "types-PyYAML"
        ]
    },
    python_requires=">=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*,!=3.5.*",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
