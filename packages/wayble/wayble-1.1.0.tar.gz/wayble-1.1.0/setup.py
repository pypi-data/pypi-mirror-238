from setuptools import setup, find_packages

with open("requirements.txt", "r") as f:
    REQUIREMENTS = [i.strip() for i in f.readlines()]

with open('README.md', 'r') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name="wayble",
    version="1.1.0",
    packages=find_packages(),
    install_requires=REQUIREMENTS,
    entry_points={
        'console_scripts': [
            'wayble=cli.cli:cli',
        ],
    },
    author="Selvin Ortiz",
    author_email="selvin@modcreativeinc.com",
    description="Official CLI for Wayble AI",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/modcreative/wayble.py",  # Change to your repository URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Change this if you're using a different license
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
