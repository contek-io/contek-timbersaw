from setuptools import setup, find_packages

setup(
    name='contek-timbersaw',
    version='0.1',
    description='Contek Python Timbersaw',
    url='https://contek.io',
    author='contek',
    author_email='dev@contek.io',
    license='private',
    packages=find_packages('.', exclude=['tests*']),
    install_requires=[],
    zip_safe=True,
)
