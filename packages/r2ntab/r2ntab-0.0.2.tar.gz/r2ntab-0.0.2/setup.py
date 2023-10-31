from setuptools import setup, find_packages

setup(
    name='r2ntab',
    version='0.0.2',
    author='M.J. van der Zwart',
    author_email='mvdzwart01@hotmail.nl',
    description='Model for binary classification combining deep learning and rule learning',
    packages=find_packages(),
    keywords=['python', 'rule learning', 'neural networks', 'deep learning', 'classification'],
    install_requires=['torch', 'torchvision', 'numpy'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
