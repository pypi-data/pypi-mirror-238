import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name="ants-pi",
    version="0.0.4",
    author="neuraldevops",
    author_email="minseok.kim@brain.snu.ac.kr",
    description="ANalysis for Time Series",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/minsmis/ANTS",
    project_urls={
        "Bug Tracker": "https://github.com/minsmis/ANTS/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "mat73>=0.62",
        "matlabengine>=23.2.1",
        "matplotlib>=3.7.2",
        "numpy>=1.26.0",
        "pandas>=2.1.1",
        "pyside6>=6.6.0",
        "scikit-learn>=1.3.0",
        "scipy>=1.11.1"
    ]
)

