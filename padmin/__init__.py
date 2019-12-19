"""padmin: project administration module
for Christophe Van Neste

... just the way I like organizing my projects,
not intended for general use.
"""
import os
import re
import subprocess as sub
from padmin import templates
from padmin.utils import multiline_input


class Project(object):
    def __init__(self, dirname='.'):
        self.location = os.getcwd() if dirname == '.' else dirname
        self.name = os.path.basename(self.location)
        if not os.path.exists(self.location):
            print(f'Initializing {self.name} ({self})')
            os.mkdir(self.location)

    def git_init(self):
        curdir = os.getcwd()
        os.chdir(self.location)
        sub.run('git init'.split())
        sub.run('git add *'.split())
        sub.run(['git', 'commit', '-m"first commit"'])
        sub.run(
            f'git remote add origin https://github.com/dicaso/{self.name}.git'
            .split())
        # Make repo on github from commandline
        sub.run([
            'curl', '-u', 'beukueb',
            # TODO add token https://github.com/settings/tokens for auth
            'https://api.github.com/orgs/dicaso/repos',
            '-d',
            f'{{"name":"{self.name}","description":"{self.description}"}}'
        ])
        # for user repo, replace /orgs/dicaso with /user
        # info https://developer.github.com/v3/repos/#create
        sub.run('git push -u origin master'.split())
        os.chdir(curdir)


class PyProject(Project):
    def __init__(self, dirname='.', description='',
                 git_init=False, pypi_init=False):
        super().__init__(dirname)
        if not os.path.exists(os.path.join(self.location, self.name)):
            print(f'preparing python files for <{self.name}>')
            self.setup_init(description, git_init=git_init,
                            pypi_init=pypi_init)

    def setup_init(self, description='', git_init=False, pypi_init=False):
        os.mkdir(os.path.join(self.location, self.name))
        self.description = description or input('Description: ')

        # README.md
        multiline_input(
            '# '+self.name, editor=True,
            filename=os.path.join(self.location, 'README.md')
        )

        # setup.py
        self.setupfile_init()

        # __init__.py
        with open(
                os.path.join(self.location, self.name, '__init__.py'), 'wt'
        ) as f:
            f.write(templates.init.format(name=self.name))

        # requirements.txt requirements-dev.txt
        # TODO

        # LICENSE
        multiline_input(
            templates.license, editor=True,
            filename=os.path.join(self.location, 'LICENSE')
        )

        # prepare git
        if git_init:
            self.git_init()

        # submit to pypi
        # prepare virtualenv
        self.mkvirtualenv()

        # install twine and pre-commit in virtualenv
        sub.run(['bash'], input=f'''.  {self.location}/.env/bin/activate
            cd {self.location}
            # twine
            pip install twine
            # pre-commit
            pip install pre-commit
            pre-commit install
        '''.encode())

        # pre-commit config
        with open(
                os.path.join(self.location, '.pre-commit-config.yaml'), 'wt'
        ) as f:
            f.write(templates.precommit)

        if pypi_init:
            self.twine()

    def push2pypi(self):
        sub.run(['bash'], input=f'''.  {self.location}/.env/bin/activate
            cd {self.location}
            python3 setup.py sdist bdist_wheel
            python3 -m twine upload dist/*
        '''.encode())

    def setupfile_init(self):
        print('Provide information for "setup.py"')
        file = SkeletonFile(
            template=f'''
            from setuptools import setup, find_packages

            with open("README.md", "r") as fh:
                long_description = fh.read()

            setup(name='{self.name}',
                  version='0.0.1',
                  description='{self.description}',
                  long_description=long_description,
                  long_description_content_type="text/markdown",
                  url='https://github.com/dicaso/{self.name}',
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
                  {multiline_input('# Requirements:', editor=True)}
                  ],
                  extras_require={{
                      'documentation': ['Sphinx']
                  }},
                  package_data={{}},
                  include_package_data=True,
                  zip_safe=False,
                  entry_points={{}},
                  test_suite='nose.collector',
                  tests_require=['nose']
                  )

            # To install with symlink, to make changes immediately available:
            # pip install -e .
            '''
        )
        file.copy(os.path.join(self.location, 'setup.py'))

    def mkvirtualenv(self):
        # installing virtualenv in hidden .env folder under root folder
        sub.run(['virtualenv',  os.path.join(self.location, '.env')])


class SkeletonFile(object):
    def __init__(self, template, settings={}, reident=True):
        if reident:
            identspace = re.compile(r'.*\n(\W*)\w')
            template = template.replace(
                '\n'+identspace.match(template).groups()[0], '\n')
        self.content = template.format(**settings) if settings else template

    def copy(self, filename):
        with open(filename, 'wt') as f:
            f.write(self.content)
