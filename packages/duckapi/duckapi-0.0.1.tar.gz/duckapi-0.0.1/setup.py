from setuptools import setup, find_packages

readme = """
# API wrapper for DuckAPI (https://github.com/Lcvb-x/DuckApi) written in Python.
"""

setup(
    name="duckapi",
    version="0.0.1",
    description="Async API wrapper for DuckAPI.",
    long_description=readme,
    author="Its-MatriX; Lcvb-x",
    url="https://github.com/Its-MatriX/duckapi-wrapper",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
        "Framework :: AsyncIO",
    ],
    keywords="api wrapper api-wrapper duck duck-api",
    install_requires=[],
    long_description_content_type="text/markdown",
)
