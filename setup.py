from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='contek-timbersaw',
    version='2.6',
    description='Timbersaw for automatic logging configuration',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=["contek_timbersaw"],
    url='https://github.com/contek-io/contek-timbersaw',
    author='contek_bjy',
    author_email='bjy@contek.io',
    license='MIT',
    install_requires=[],
    zip_safe=True,
)
