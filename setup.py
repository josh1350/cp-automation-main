import os
import setuptools
from setuptools import find_packages

# setup(
#     packages=find_packages()
# )

here = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(here, "src", "ui", "__version__.py")) as about_file:
    exec(about_file.read(), about)
python_version = ">=3.9"
with open(os.path.join(here, "README.md"), encoding="UTF-8") as readme_file:
    readme = readme_file.read()


setuptools.setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=readme,
    packages=find_packages(),
    python_version=python_version,
)