from setuptools import setup, find_packages

package_data = {
    "translate": ["libparser.so"],
}

setup(
    name='translate',
    version='3.2.1',    
    description='Translate your input in real time',
    packages=find_packages(),
    include_package_data=True,
    package_data=package_data,
    python_requires=">=3.7",
)

