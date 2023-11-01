import setuptools
import re

with open("README.md", "r") as fh:
    readme_lines = fh.readlines()
    long_description = " ".join(readme_lines)
    print(readme_lines)
    version_history_start = [l[0] for l in enumerate(readme_lines) if "Version history" in l[1]][0]
    latest_version = re.search("\d+?\.\d+?", readme_lines[version_history_start+1:][0])[0]

setuptools.setup(
    name="sddk", # Replace with your own username
    version=latest_version,
    author="Vojtech Kase",
    author_email="vojtech.kase@gmail.com",
    description="A package to access sciencedata.dk",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sdam-au/sddk",
    packages=setuptools.find_packages(),
    install_requires=[
        "pyarrow", # >=3",
        "plotly",
        #"kaleido>=0.2.1",
        "beautifulsoup4>=4",
        "pandas>=1",
        "numpy>=1",
        "requests>=2",
        "matplotlib>=3.3.4",
        "geopandas",
        "shapely"
        ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
)
