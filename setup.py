from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["beautifulsoup4>=4.10.0",
                "selenium>=4.1.0", "ordered-set>=4.0.2"]

setup(
    name="dolos",
    version="0.0.1",
    author="ReiseArnor",
    author_email="odanisdejesus@gmail.com",
    description="Programa en Python 3 para ver anime sin anuncios desde la terminal",
    long_description=readme,
    long_description_content_type="text/markdown",
    # url="https://github.com/your_package/homepage/",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT",
    ],
    entry_points={
        'console_scripts': [
            "dolos=dolos.dolos:start"
        ],
    },
)
