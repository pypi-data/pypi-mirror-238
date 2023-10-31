from distutils.core import setup
from setuptools import find_packages


description = """
Python library to analyze and plot network graphs.
"""

with open("README.md") as f:
    long_description = f.read()

with open("requirements.txt") as f:
    install_requires = f.read().splitlines()

setup(
    name="graph_express",
    version="0.1.0a1.dev2",
    description=description.strip(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=install_requires,
    url="https://github.com/nelsonaloysio/graph-express",
    author=["Nelson Aloysio Reis de Almeida Passos"],
    license="MIT",
    keywords="network graph",
    python_requires=">=3",
    package_dir={"": "src"},
    packages=find_packages(
        where="src",
        exclude=["build.*", "test.*"]
    ),
    project_urls={
        "Source": "https://github.com/nelsonaloysio/graph_express",
        "Tracker": "https://github.com/nelsonaloysio/graph_express/issues",
    },
    entry_points={
        "console_scripts": [
            "graph-express = graph_express.cli:main"
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
