from setuptools import setup, find_packages
from pathlib import Path

VERSION = "2.1.5"
DESCRIPTION = "En SDK til gymnasie siden Lectio, lavet af jona799t"
long_description = (Path(__file__).parent / "README.md").read_text()

# Setting up
setup(
    name="python-lectio-unbloated",
    version=VERSION,
    author="JohnnyJTH",
    # author_email="<not@available.com>",
    url="https://github.com/JohnnyJTH/python-lectio",
    description=DESCRIPTION,
    long_description=long_description,
    license_files=("LICENSE.txt",),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["requests", "beautifulsoup4", "markdownify"],
    keywords=["python", "lectio", "sdk", "gymnasie", "gymnasium"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
