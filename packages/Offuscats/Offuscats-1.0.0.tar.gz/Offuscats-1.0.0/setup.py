import setuptools, os

# create commande for upload projet to Pypi



with open("README.md", "r") as f:
    LONG_DESCRIPTION = f.read()

setuptools.setup(
    name="Offuscats",
    version="1.0.0",
    license="apache-2.0",
    author="TryWarz",
    author_email="trywarz@trywarz.online",
    url="https://github.com/TryWarzFiles/Offuscat",
    keywords="obfuscation, obfuscate, obfuscator, obfuscating, obfuscated, obfuscates, obfuscators",
    description="A Python obfuscator. Github official : https://github.com/TryWarzFiles/Offuscat",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=["Offuscat"],
)