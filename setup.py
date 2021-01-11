from setuptools import setup, find_packages


with open("README.md") as f:
    readme = f.read()

with open("LICENSE") as f:
    license = f.read()


def read_requirements():
    """Parse requirements from requirements.txt."""
    reqs_path = os.path.join(".", "requirements.txt")
    with open(reqs_path, "r") as f:
        requirements = [line.rstrip() for line in f]
    return requirements


version = None
with open("to4326/__init__.py", "r") as fp:
    for line in fp:
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip("\"'")
            break

setup(
    name="to4326",
    version=str(version),
    description="transform geometry points to EPSG:4326",
    long_description=readme,
    packages=[
        "to4326",
        "to4326.transform",
        "to4326.calc",
        "to4326.lonlat",
        "to4326.types",
        "to4326.validate",
    ],
    author="yonda",
    author_email="yonda.fountain@gmail.com",
    url="https://github.com/yonda-yonda/to4326",
    license=license,
    install_requires=read_requirements(),
)