from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / 'README.md').read_text()
  
setup(
    name = 'multipoly',
    version = '0.9.1',
    description = 'A multivariate polynomial module.',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    
    author = 'Sebastian Gössl',
    author_email = 'goessl@student.tugraz.at',
    license = 'MIT',
    
    py_modules = ['multipoly'],
    url = 'https://github.com/goessl/multipoly',
    python_requires = '>=3.6',
    install_requires = ['numpy'],
    
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Mathematics'
    ]
)
