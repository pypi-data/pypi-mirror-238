from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_desc = fh.read()

setup(
    name="mkdocs_cu_ab6459",
    version="0.0.8",
    url='https://github.coventry.ac.uk/ab6459/mkdocs_cu_ab6459',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Topic :: Documentation',
        'Topic :: Text Processing',
    ],
    install_requires=[
        'mkdocs',
    ],
    license='MIT',
    description='Improved and extended version of the Windmill theme',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    author='Ian Cornelius',
    author_email='ab6459@coventry.ac.uk',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'mkdocs.themes': [
            'cu-ab6459 = mkdocs_cu_ab6459',
        ]
    },
    zip_safe=False
)