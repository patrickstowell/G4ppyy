from setuptools import setup, find_packages

setup(
    name='g4ppyy',
    version='0.1.0',
    author='Patrick Stowell',
    author_email='p.stowell@sheffield.ac.uk',
    description='Python binding helper tools for G4 and CPPYY',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/patrikstowell/G4ppyy',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
    install_requires=[
        'numpy',
        'k3d',
        'matplotlib'
    ],
)

