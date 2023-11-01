from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='PowerScrape',
    version='0.1.2',
    author='ohioman02',
    author_email='gdnunuuwu@gmail.com',
    description='A comprehensive and versatile Python module for web scraping.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/RoseInjector/PowerScrape/',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests',
        'beautifulsoup4',
        'selenium',
        'pdfplumber',
        'Pillow',
        'pytesseract',
        'opencv-python',
        'numpy',
        'cachetools',
    ],
)
