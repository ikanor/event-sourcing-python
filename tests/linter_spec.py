import os
import subprocess
import sys

import pep8
from expects import expect, equal

EXCLUDED_FILES = []
INCLUDED_FILES = ['src', 'tests']


def root_path():
    this_path = os.path.normpath(os.path.dirname(__file__))
    return os.path.abspath(os.path.join(this_path, os.pardir, os.pardir))


def get_excluded_files():
    result = []
    for path in EXCLUDED_FILES:
        result.append(os.path.join(root_path(), path))
    return result


def get_config_file():
    return os.path.join(root_path(), 'linter.cfg')


with description('Test Code Conformation'):
    with it('should conform PEP8'):
        pep8style = pep8.StyleGuide(
            config_file=get_config_file(), exclude=get_excluded_files())
        result = pep8style.check_files(INCLUDED_FILES)
        expect(result.total_errors).to(equal(0))
