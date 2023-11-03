from setuptools import setup, find_packages

with open("requirements.txt", "r") as f:
    required = f.read().splitlines()

setup(
    name="neuroseg",
    version="0.1.2",
    packages=find_packages(),
    author="Allen Institute for Brain Science",
    # setup_requires=["pytest-runner"],
    # tests_require=["pytest"],
    description="A PyTorch-based framework for deep learning in neuroscience",
    install_requires=required,
    include_package_data=True,
)
