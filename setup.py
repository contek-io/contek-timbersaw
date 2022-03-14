from setuptools import setup, find_packages

setup(
    name='contek-tusk',
    version='0.1',
    description='Contek Python Tusk',
    url='https://contek.io',
    author='contek',
    author_email='dev@contek.io',
    license='private',
    packages=find_packages('.', exclude=['tests*']),
    install_requires=[
        'clickhouse-driver',
        'pandas',
    ],
    zip_safe=True,
)
