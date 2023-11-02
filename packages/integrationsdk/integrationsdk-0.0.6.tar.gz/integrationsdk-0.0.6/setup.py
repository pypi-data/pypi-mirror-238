"""cookiecutter distutils configuration."""
from pathlib import Path
from setuptools import setup, find_packages


version = "0.0.6"


with open('README.md', encoding='utf-8') as readme_file:
    readme = readme_file.read()


requirements = [
    'binaryornot>=0.4.4',
    'Jinja2>=2.7,<4.0.0',
    'click>=7.0,<9.0.0',
    'pyyaml>=5.3.1',
    'python-slugify>=4.0.0',
    'requests>=2.23.0',
    'arrow',
    'rich',
    'cookiecutter'
]


setup(
    name='integrationsdk',
    version=version,
    description=(
        'A command-line utility that creates Python package project template.'
        'This newly created project will have boiler plate code for integrations.'
    ),
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Ashish Gupta',
    author_email='ashishkrgupta@hotmail.com',
    url='https://github.com/ashishkrgupta/python-starter-template',
    project_urls={
        "Documentation": "https://cookiecutter.readthedocs.io",
        "Issues": "https://github.com/cookiecutter/cookiecutter/issues"
    },
    packages=find_packages(exclude=[]),
    package_dir={'integrationsdk': 'integrationsdk'},
    entry_points={'console_scripts': ['integrationsdk = integrationsdk.__main__:main']},
    include_package_data=True,
    python_requires='>=3.7',
    install_requires=requirements,
    license='BSD',
    zip_safe=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: Python",
        "Topic :: Software Development",
    ],
    keywords=[
        "itegration-sdk",
        "Python",
        "projects",
        "project templates",
        "project directory",
        "package",
        "packaging",
    ],
)