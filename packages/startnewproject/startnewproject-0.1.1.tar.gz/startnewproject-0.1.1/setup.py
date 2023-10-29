import subprocess
from setuptools import setup, find_packages
from setuptools.command.install import install
from startnewproject import __version__
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

class PostInstallCommand(install):
    def run(self):
        try:
            subprocess.check_output(['git', '--version'])
        except FileNotFoundError:
            red = '\033[0;31m'
            raise SystemExit(f"{red}Git is not installed. Please install Git on your system.")
        install.run(self)
    
setup(
    name='startnewproject',
    version=__version__,
    description="This package provides a command to create a new project folder with subfolders, READMEs, pylabnotebook and git.",
    long_description=long_description,
    long_description_content_type='text/markdown',

    author="Matteo Miotto",
    author_email="miotsdata@gmail.com",
    
    packages=find_packages(),
    package_data={'startnewproject': ['templates/*']},
    entry_points={
        'console_scripts': [
            'startnewproject = startnewproject.main:main',
        ],
    },
    cmdclass={
        'install': PostInstallCommand,
    },
    install_requires=[
        "argparse",
        "pylabnotebook>=0.1.4"
    ],
)
