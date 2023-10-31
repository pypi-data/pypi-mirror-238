from pathlib import Path

from setuptools import setup
from setuptools import find_packages

# Settings
NAME = 'simlog'
FILE = Path(__file__).resolve()
PARENT = FILE.parent  # root directory

about = {}
exec((PARENT / NAME / '__version__.py').read_text(encoding='utf-8'), about)
DESCRIPTION = 'A simple logging package'
README = (PARENT / 'README.md').read_text(encoding='utf-8')

setup(
    name=NAME,
    version=about['__version__'],
    author='Olalaye',
    url='https://github.com/Olalaye/slog',
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type='text/markdown',
    install_requires=[],
    license='GPL-3.0',
    packages=find_packages(),
    
    keywords=['python', 'loggong', 'simlog', 'log'],
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        'Operating System :: POSIX :: Linux',
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Software Development :: Libraries"
    ]
)