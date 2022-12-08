from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='HeapQueue',
    version='0.0.1',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/AlexanderChiuy/HeapQueue',
    py_modules=[],
    packages=["HeapQueue"]
)
