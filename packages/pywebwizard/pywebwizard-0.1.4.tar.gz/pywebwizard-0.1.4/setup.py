from setuptools import setup, find_packages

with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

setup(
    name="pywebwizard",
    version="0.1.4",
    description="Magic Browser library",
    long_description=open('README.md', 'r').read(),
    long_description_content_type="text/markdown",
    author="Parendum OÜ",
    author_email="info@parendum.com",
    url="https://github.com/tuusuario/webwizard",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
)
