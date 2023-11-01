import setuptools
import os

try:
    with open("ActflowToolbox/README.md", "r", encoding = "utf-8") as fh:
        long_description = fh.read()
except:
    long_description = ""

try :
    with open("ActflowToolbox/LICENSE", "r", encoding = "utf-8") as fh:
        license_text = fh.read()
except:
    license_text = ""

setuptools.setup(
    name = "actflow",
    version = "0.3.2",
    author = "Michael Cole",
    author_email = "michael.cole@rutgers.edu",
    description = "The Brain Activity Flow (Actflow) Toolbox. Tools to quantify the relationship between connectivity and task activity through network simulations and machine learning prediction. Helps determine how connections contribute to specific brain functions.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/ColeLab/ActflowToolbox",
    packages=setuptools.find_packages(),
    install_requires = [
        'gglasso',
        'wbplot',
        'seaborn',
        'gglasso',
        'matplotlib',
        'numpy<1.24',
        'h5py',
        'statsmodels',

    ],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    license=license_text,
    # package_dir = {"": "src"},
    python_requires = ">=3.0"
)