from time import time
import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name='abstract_gui',
    version='0.0.61.38',
    author='putkoff',
    author_email='partners@abstractendeavors.com',
    description='abstract_gui is a python module for creating abstract GUI windows and interacting with them. It uses the PySimpleGUI library and provides additional utilities for simplifying the creation and handling of PySimpleGUI windows.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/AbstractEndeavors/abstract_essentials/tree/main/abstract_gui',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
    ],
    install_requires=['abstract_utilities>=0.2.2.1', 'abstract_gui>=0.0.58.8', 'PySimpleGUI>=4.60.5'],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    # Add this line to include wheel format in your distribution
    setup_requires=['wheel'],
)
