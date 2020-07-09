import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
ㅎ
setuptools.setup(
    name="aiotime",
    version="0.1.0",
    author="Arseniy Banayev",
    author_email="arseniy.banayev@gmail.com",
    description="Test helper for controlling the asyncio event loop's internal clock",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="asyncio async time sleep",
    url="https://github.com/arseniybanayev/aiotime",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6"
)