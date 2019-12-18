"""Utilities for
padmin package
"""
import os
import subprocess as sub


def multiline_input(prompt=None, editor=False, filename=None):
    import sys
    import tempfile
    if editor:
        tmpfile = (
            open(filename, 'wt') if filename else
            tempfile.NamedTemporaryFile(mode='w+t', delete=False)
        )
        tmpname = filename if filename else tmpfile.name
        if prompt:
            tmpfile.write(prompt)
        tmpfile.close()
        try:
            editor = os.environ['editor']
        except KeyError:
            editor = 'vi'
        sub.run([editor, tmpname])
        with open(tmpfile.name) as inpfile:
            content = ''.join(inpfile.readlines())
        if not filename:
            os.remove(tmpfile.name)
    else:
        if prompt:
            print(prompt)
        content = ''.join(sys.stdin.readlines())
    return content
