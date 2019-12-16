"""padmin: project administration module
for Christophe Van Neste

... just the way I like organizing my projects,
not intended for general use.
"""
import os
import re
import subprocess as sub
from padmin import templates

def multiline_input(prompt=None, editor=False, filename=None):
    import sys
    import tempfile
    if editor:
        tmpfile = (
            open(filename, 'wt') if filename else
            tempfile.NamedTemporaryFile(mode='w+t', delete=False)
        )
        tmpname = filename if filename else tmpfile.name
        if prompt: tmpfile.write(prompt)
        tmpfile.close()
        try: editor = os.environ['editor']
        except KeyError: editor = 'vi'
        sub.run([editor, tmpfile.name])
        with open(tmpfile.name) as inpfile:
            content = ''.join(inpfile.readlines())
        if not filename: os.remove(tmpfile.name)
    else:
        if prompt: print(prompt)
        content = ''.join(sys.stdin.readlines())
    return content

class Project(object):
    def __init__(self, dirname):
        self.name = os.path.basename(dirname)
        self.location = dirname
        #os.mkdir(dirname)

    def git(self):
        curdir = os.getcwd()
        os.chdir(self.location)
        sub.run('git init'.split())
        sub.run('git add *'.split())
        sub.run(['git', 'commit', '-m"first commit"'])
        os.chdir(curdir)

class PyProject(Project):
    def __init__(self, dirname):
        super().__init__(dirname)
        #os.mkdir(os.path.join(self.location, self.name))

        # README.md
        multiline_input(
            '# '+self.name, editor = True,
            filename = os.path.join(self.location, self.name, 'README.md')
        )

        # setup.py
        self.setupfile()

        # LICENSE
        multiline_input(
            templates.license, editor=True,
            filename = os.path.join(self.location, self.name, 'LICENSE')
        )

        # prepare git
        self.git()
        
    def setupfile(self):
        print('Provide information for "setup.py"')
        file = SkeletonFile(
            template = f'''
            from setuptools import setup, find_packages
            
            with open("README.md", "r") as fh:
                long_description = fh.read()
            
            setup(name='{self.name}',
                  version='0.0.1',
                  description='{input('Description: ')}',
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
            
            # To install with symlink, so that changes are immediately available:
            # pip install -e .
            '''
        )
        file.copy(os.path.join(self.location, 'setup.py'))

class SkeletonFile(object):
    def __init__(self, template, settings={}, reident=True):
        if reident:
            identspace = re.compile(r'.*\n(\W*)\w')
            template = template.replace('\n'+identspace.match(template).groups()[0],'\n')
        self.content = template.format(**settings) if settings else template

    def copy(self, filename):
        with open(filename, 'wt') as f:
            f.write(self.content)
