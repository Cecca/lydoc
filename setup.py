from setuptools import setup, find_packages
import io


version = dict()
with io.open("lydoc/_version.py", "r", encoding='utf-8') as fp:
    exec(fp.read(), version)

with io.open("README.rst", "r", encoding='utf-8') as fp:
    long_desc = fp.read()

setup(
    name='lydoc',
    version=version['__version__'],
    author='Matteo Ceccarello',
    author_email='matteo.ceccarello@gmail.com',
    license='GPLv3',
    url='https://github.com/Cecca/lydoc',
    description='An API documentation generator for Lilypond files',
    long_description=long_desc,
    packages=find_packages(exclude=['docs', 'tests*']),
    include_package_data=True,
    install_requires=[
        'jinja2',
        'grako'
    ],
    extras_require={
        'dev': ['pyinstaller'],
        'test': ['coverage', 'nose'],
    },
    classifiers={
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Development Status :: 3 - Alpha",
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    },
    entry_points={
        'console_scripts': [
            'lydoc=lydoc:main'
        ]
    }
)
