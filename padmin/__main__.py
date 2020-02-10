"""CLI module
different functions that are exposed on the terminal
"""

import os
import argparse
from argetype import ConfigBase


def main():
    class Settings(ConfigBase):
        action: str                 # Options: create, workon, commit
        name: str = '.'             # Project name TODO optional last argument
        projecttype: str = 'python'  # Options: python, pywebapp
        private: bool = False       # Do not submit to git or pypi
    settings = Settings(parse=True)

    if settings.action == 'create':
        from padmin import PyProject
        if settings.projecttype in ('python', 'pywebapp'):
            PyProject(
                dirname=settings.name,
                git_init=not(settings.private),
                pypi_init=not(settings.private),
                web=settings.projecttype == 'pywebapp'
            )
        else:
            print('Unknown project type', settings.projecttype)
    else:
        print(settings, 'not implemented yet')


def pad_commit():
    pass


def workon():
    import argcomplete

    def ProjectCompleter(**kwargs):
        import glob
        return [
            os.path.basename(d)
            for d in glob.glob(os.path.expanduser('~/repos/*'))
        ]
    parser = argparse.ArgumentParser()
    parser.add_argument("project").completer = ProjectCompleter
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    os.chdir(os.path.expanduser(f'~/repos/{args.project}'))
    print(os.getcwd())
    # TODO not working according to plan yet
    cmd = [
        'bash', '-c',
        f'source ~/repos/{args.project}/.env/bin/activate && bash'
    ]
    os.execvp(cmd[0], cmd)


def mkpyproject():
    pass


if __name__ == '__main__':
    main()
