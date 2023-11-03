from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
import os


setup(
    packages = find_packages(where="src"),
    package_dir = {"": "src"},
    include_package_data=True,
    data_files=[("NaxToPy", ["src/NaxToPy/NaxToPy.ico"])],
    url="https://idaerosolutions.com/",
    download_url="https://appsource.microsoft.com/en-us/product/SaaS/idaerosolutionssl1685692009813.naxto?signInModalType=2&ctaType=1"
)