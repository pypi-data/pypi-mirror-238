import codecs
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0.1'
DESCRIPTION = 'A package for easy plotting 3D Polygons in matplotlib.'

setup(
    name="VisualShape3D",
    version=VERSION,
    author="Liqun He",
    author_email="heliqun@ustc.edu.cn",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    license='MIT',
    url = 'https://pypi.org/project/VisualShape3D/',
    keywords=['python', 'VisualShape3D','windows','mac','linux'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
