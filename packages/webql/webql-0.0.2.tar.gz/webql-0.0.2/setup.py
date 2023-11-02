from setuptools import setup

with open("PACKAGE_README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="webql",
    version="0.0.2",
    description="Tiny Fish WebQL Python Client",
    python_requires=">=3.11",
    install_requires=["playwright>=1,<2", "requests>=2,<3"],
    packages=["webql"],
    package_dir={"": "src"},
    long_description=long_description,
    long_description_content_type="text/markdown",
)
