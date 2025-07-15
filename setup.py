from setuptools import find_packages, setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()
    
setup(
    name="AI_Medical_Chatbot",
    version="0.1",
    author="Jai Vadula",
    packages=find_packages(),
    install_requires = requirements,
)
