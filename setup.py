
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='padmin',
      version='0.0.1',
      description='Project administration tool',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/dicaso/padmin',
      author='Christophe Van Neste',
      author_email='christophe.vanneste@kaust.edu.sa',
      license='MIT',
      packages=find_packages(),
      python_requires='>=3.6',
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: POSIX",
          "Development Status :: 1 - Planning"
      ],
      install_requires=[
          'virtualenv',
          'argcomplete',
          'argetype',
          'kindi'
      ],
      extras_require={
          'documentation': ['Sphinx']
      },
      package_data={},
      include_package_data=True,
      zip_safe=False,
      entry_points={
          'console_scripts': [
              'pad=padmin.__main__:main',
              'pad-commit=padmin.__main__:pad_commit',
              'porkon=padmin.__main__:workon',
              'mkpyproject=padmin.__main__:pyproject'
          ],
      },
      test_suite='nose.collector',
      tests_require=['nose']
      )

# To install with symlink, so that changes are immediately available:
# pip install -e .
