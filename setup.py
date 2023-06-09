from setuptools import find_packages, setup
from typing import List

HYPEN_E_DOT = "-e ."

def get_requirements(filepath:str)->List[str]:

    requirements = []
    with open(filepath) as file_obj:
        requirements = file_obj.readlines() # there /n is available for line by line, so we should replace it
        requirements = [req.replace("\n", "") for req in requirements]

        if HYPEN_E_DOT in requirements:     
            requirements.remove(HYPEN_E_DOT)

    return requirements


setup(
    name = "Diamond Price Prediction Project",
    version = "0.0.1",
    author = "Santhosh Kumar",
    author_email = "santhoshbharath61@gmail.com",
    install_requires = get_requirements('requirements.txt'),
    packages = find_packages()
)