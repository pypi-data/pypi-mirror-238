import codecs
import os

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = "0.0.6"
DESCRIPTION = "Basic util library for progress bar and cron trigger and mssql db check related operation"
LONG_DESCRIPTION = """A package that allows to build schedule Triggers based on quartz cron expression,
    to build a simple Progressbar and mssql db connection checker"""

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
    install_requires=["colorama>=0.4.6", "cron-schedule-triggers>=0.0.11", "pydantic>=1.10.4", "pyodbc>=4.0.35", "pywin32>=306", "win32security>=2.1.0"],
    keywords=[
        "python",
        "psvutils",
        "quartz",
        "quartzcron",
        "quartz cron",
        "cron",
        "cron triggers",
        "quartzcron triggers",
        "mssql_db_check",
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
