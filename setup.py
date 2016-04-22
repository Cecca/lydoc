from setuptools import setup, find_packages

version = dict()
with open("lydoc/_version.py", "r") as fp:
    exec(fp.read(), version)

with open("README.md", "r", encoding='utf-8') as fp:
    long_desc = fp.read()

setup(
    name='lydoc',
    version=version['__version__'],
    author='Matteo Ceccarello',
    author_email='matteo.ceccarello@gmail.com',
    license='GPLv3',
    url='TODO',
    description='An API documentation generator for Lilypond files',
    long_description=long_desc,
    packages=find_packages(exclude=['docs', 'tests*']),
    install_requires=[
        'jinja2',
        'grako'
    ],
    extras_require={
        'dev': ['pyinstaller'],
        'test': ['coverage', 'nose'],
    },
    entry_points = {
        'console_scripts': [
            # TODO
        ]
    }
)
