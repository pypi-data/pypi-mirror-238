import setuptools

with open("README.md", "r", encoding="utf-8") as fp:
    readme = fp.read()

setuptools.setup(
    name="flask_file_router",
    version="0.0.1",
    author="Kaushal Prasad Balmiki",
    description="File Based Routing for Flask Server",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/kaush26/flask-file-router",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['Flask'],
    keywords=['File Router', 'Flask', 'API', 'Python', 'Server'],
    python_requires=">=3.7",
)
