from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='afdd',
    version='0.0.1',
    description='A python package for automated fault detection and diagnosis',
    url='https://github.com/shuds13/pyexample',
    author='Roberto Chiosa',
    author_email='roberto.chiosa@polito.it',
    license='BSD 2-clause',
    packages=['afdd'],
    install_requires=['mpi4py>=2.0',
                      'numpy',
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)