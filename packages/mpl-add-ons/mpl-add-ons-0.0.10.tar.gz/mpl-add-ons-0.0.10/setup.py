from setuptools import setup, find_packages
# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="mpl-add-ons",
    version='0.0.10',
    author="Ethan Blake",
    long_description=long_description,
    long_description_content_type='text/markdown',
    description="Helper functions to make using matplotlib easier, more efficient and streamlined",
    packages=find_packages(),
    install_requires=['matplotlib', 'PyQt5', 'ttkbootstrap', 'Pillow', 'pywin32']
)
