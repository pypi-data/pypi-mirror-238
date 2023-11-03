from setuptools import setup


PACKAGE_NAME = 'act4'

VERSION = '3.2.0'

REQUIRES = ('pyannotating==1.3.0', )

with open('README.md') as readme_file:
    LONG_DESCRIPTION = readme_file.read()

setup(
    name=PACKAGE_NAME,
    description="Library for metaprogramming",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license_files=('LICENSE', ),
    license='GNU General Public License v3.0',
    version=VERSION,
    install_requires=REQUIRES,
    url="https://github.com/TheArtur128/Act",
    download_url=(
        "https://github.com/TheArtur128/Act"
        f"/archive/refs/tags/v{VERSION}.zip"
    ),
    author="Arthur",
    author_email="s9339307190@gmail.com",
    python_requires='>=3.11',
    classifiers=['Programming Language :: Python :: 3.11'],
    keywords=[
        "monads", "library", "pipeline", "functional-programming", "utils",
        "lambda-functions",  "metaprogramming", "annotations", "immutability",
        "algebraic-data-types", "error-handling", "duck-typing", "currying",
        "object-proxying", "functors", "contextualization", "utils-library",
        "endofunctors",  "pseudo-operators", "structural-oop"
    ],
    packages={'act': 'act4', 'act.cursors': 'act4.cursors'},
)
