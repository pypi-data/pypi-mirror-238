from setuptools import setup

__version__ = "0.0.0"  # for type hinting
exec(open("pqapi/version.py").read())

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pqapi",
    version=__version__,  # noqa
    description="API for interacting with paperqa.app",
    author="Andrew White",
    author_email="andrew@futurehouse.org",
    url="https://github.com/Future-House/pqapi",
    license="MIT",
    packages=["pqapi"],
    install_requires=[
        "requests",
        "pydantic",
        "paper-qa",
        "tenacity",
        "aiohttp",
        "jinja2",
    ],
    test_suite="tests",
    long_description=long_description,
    entry_points={
        "console_scripts": [
            "pqa-render=pqapi.main:main",
        ],
    },
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
