from setuptools import setup, find_packages

setup(
    name='process-twarc',
    version='0.18.9',
    license='MIT',
    description='Tools for tranforming raw data from Twarc2 to structured data for Masked Language Modeling.',
    author='Jordan Wolfgang Klein',
    author_email='jordan.klein.21@um.edu.mt',
    url='https://github.com/user/Lone-Wolfgang',
    keywords=['Twitter', 'Deduplication', 'Tokenization', 'Language Modeling'],
    install_requires=[
        'pyarrow',
        'transformers',
        'pandas',
        'datasets'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ],
    packages=find_packages(),
)
