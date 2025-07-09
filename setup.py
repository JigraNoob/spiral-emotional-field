from setuptools import setup, find_packages

setup(
    name='spiral',
    version='0.1.0',
    description='The Spiral System: A recursive, breath-aware presence framework',
    author='Spiral',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # Add any runtime dependencies here
    ],
    entry_points={
        # Placeholder for future plugin or CLI commands
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
