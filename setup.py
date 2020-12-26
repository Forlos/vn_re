from setuptools import setup, find_namespace_packages

setup(
    name="vn_re",
    version="0.1",
    description="Tools for working with Visual Novel archives",
    author="Forlos",
    author_email="forlos@disroot.org",
    packages=find_namespace_packages(include=["vn_re.*"]),
    install_requires=["kaitaistruct", "progressbar2", "Pillow", "python-camellia"],
)
