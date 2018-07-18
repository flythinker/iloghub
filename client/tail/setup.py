import codecs
import os
import re
import sys

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]",
        version_file,
        re.M,
    )
    if version_match:
        return version_match.group(1)

    raise RuntimeError("Unable to find version string.")

print(find_packages(
        where="src",
        exclude=["contrib", "docs", "tests*", "tasks"],
        include=('*',)
    ))

long_description = read('README.md')

setup(
    name="iloghub.itail",
    version=find_version("src","tail", "__init__.py"),
    description="a instance log tail tool for iloghub",
    long_description=long_description,
    license='MIT',
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Build Tools",
    ],
    url='https://github.com/flythinker/iloghub',
    keywords='"iloghub itail log java flythinker"',

    author='flythinker',
    author_email='67495224@qq.com',
    package_dir={"": "src"},
    packages=find_packages(
        where="src",
        exclude=["contrib", "docs", "tests*", "tasks"],
        include=('*',)
    ),
    package_data={
  #      "pip._vendor.certifi": ["*.pem"],
   #     "pip._vendor.requests": ["*.pem"],
    #    "pip._vendor.distlib._backport": ["sysconfig.cfg"],
    #    "pip._vendor.distlib": ["t32.exe", "t64.exe", "w32.exe", "w64.exe"],
    },
    entry_points={
        "console_scripts": [
            "itail=tail.itail:main",
        ],
    },
    zip_safe=False,
    python_requires='>=3.6',
)