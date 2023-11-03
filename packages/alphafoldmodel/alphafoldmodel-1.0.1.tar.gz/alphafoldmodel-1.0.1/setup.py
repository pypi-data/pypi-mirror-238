from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="AlphafoldModel",
    version="0.20",
    packages=find_packages(),

    # Metadata
    author="Elbert Timothy",
    author_email="ignatiuselbert5@gmail.com",
    description="A module to parse Alphafold PDB files alongside their JSON PAE matrices into interactive Python objects.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/AlphafoldModel.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
    py_modules=["alphafoldmodel/__init__","alphafoldmodel/AlphafoldModel","alphafoldmodel/ModelPDB","alphafoldmodel/ModelPAE","alphafoldmodel/LoadedKDTree"],
    package_dir={
        "": "src/AlphafoldModel"
        },
    install_requires=required
)

