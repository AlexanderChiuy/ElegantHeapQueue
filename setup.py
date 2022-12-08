from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='elegant-heap-queue',
    version='1.0.0',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/AlexanderChiuy/ElegantHeapQueue',
    packages=["elegant_heap_queue"]
)
