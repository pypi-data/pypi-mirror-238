from setuptools import setup, find_packages


with open('README.md', 'r') as file:
    long_description = file.read()

setup(
    name='magicsq',
    version='0.1',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        'numpy',
        'pandas',
    ],
    entry_points={
        'console_scripts': [
            'demo_nqueens=magicsq.demo_nqueens:main',
            'demo_eulerbox=magicsq.demo_eulerbox:main',
            'demo_bachet_box=magicsq.demo_bachet_box:main',
        ],
    },
    author='Darshan Patil',
    author_email='drshnp@outlook.com',
    description='A package for magic squares and N-Queens problem.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/1darshanpatil/magicsq_project',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
)
