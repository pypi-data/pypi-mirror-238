import setuptools

setuptools.setup(
    name = 'test_framework',
    version = '0.0.1',
    author = 'thom_dimarco',
    author_email = 'thomas.dimarco@ispot.tv',
    description = 'Python package example',
    packages = [],
    install_requires = [],
    license="MIT",
    extras_require={"dev": ["pytest >=7.0", "twine>=4.0.2"]}
)