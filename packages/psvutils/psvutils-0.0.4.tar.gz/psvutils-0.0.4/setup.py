import codecs
import os

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = "0.0.4"
DESCRIPTION = "Basic util library for progress bar and cron trigger related operation"
LONG_DESCRIPTION = """A package that allows to build schedule Triggers based on quartz cron expression,
    to build a simple Progressbar"""

# Setting up
setup(
    name="psvutils",
    version=VERSION,
    author="Pritam Sarkar 1995",
    author_email="<pritamsarkar84028220@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=["colorama>=0.4.6", "cron-schedule-triggers>=0.0.11"],
    keywords=[
        "python",
        "psvutils",
        "quartz",
        "quartzcron",
        "quartz cron",
        "cron",
        "cron triggers",
        "quartzcron triggers",
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
