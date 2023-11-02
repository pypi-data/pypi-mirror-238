from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='r2ntab',
    version='1.0.0',
    author='M.J. van der Zwart',
    author_email='mvdzwart01@hotmail.nl',
    description='Interpretable machine learning model for binary classification combining deep learning and rule learning',
    long_description=readme(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    package_dir={'r2ntab' : 'r2ntab'},
    keywords=['python', 'rule learning', 'neural networks', 'deep learning', 'classification'],
    install_requires=['torch', 'torchvision', 'numpy', 'tqdm', 'pandas', 'scikit-learn', 'scipy'],
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
