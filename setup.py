import sys

PYTHON_VERSION = sys.version_info[:3]
if PYTHON_VERSION < (3, 8):
    print("The current version of plenty does not support less " "than Python3.8")
    exit(0)

try:
    LONG_DESCRIPTION = open("README.md", encoding="utf-8").read()
except Exception:
    LONG_DESCRIPTION = """# plenty

unknown
    """

from setuptools import setup, find_packages
import plenty.info as info

setup(
    name=info.PROJECT,
    version=info.VERSION,
    author=info.AUTHOR,
    author_email=info.EMAIL,
    description=info.DESC,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS",
        # "Operating System :: Microsoft :: Windows",
    ],
    install_requires=[],
    python_requires=">=3.8",
)
