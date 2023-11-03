from setuptools import setup, find_packages
def parse_requirements(requirements):
    with open(requirements) as f:
        return [l.strip('\n') for l in f if l.strip('\n') and not l.startswith('#')]

reqs = parse_requirements("jrvc/requirements.txt")

setup(
    name='jrvc',
    description="Libraries for RVC inference",
    author_email="hugo.gonzalezdev@gmail.com",
    version='0.0.1dev010',
    packages=find_packages(),
    include_package_data=True,
    author="RVC Community",
    license="MIT",
    install_requires=reqs,
    keywords=["RVC", "Retrieval","Voice", "AI", "Conversion"],
    python_requires=">=3.8"
)