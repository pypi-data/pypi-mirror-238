# -*- coding: utf-8 -*-

import pytest

import os
import shutil

ROOT_PATH = os.path.dirname(__file__)+'/..'

def _setup_example(testdir, example_dir):
    shutil.copytree(os.path.join(ROOT_PATH, example_dir, 'src'),
                    os.path.join(str(testdir), 'src'))
    shutil.copyfile(os.path.join(ROOT_PATH, example_dir, 'test_src.py'),
                    os.path.join(str(testdir), 'test_src.py'))


@pytest.mark.parametrize('example_dir, pytest_args_donde, pytest_args_pitch, expected_nodeids_ordered, expected_nodeids_random', [
    ('examples/example01', tuple(), tuple(), [
            'test_src.py::test_f[1-1-1--2]',
            'test_src.py::test_f[1-1-0-16]',
            'test_src.py::test_f[1-0-1-0]',
            'test_src.py::test_f[0-1-1--8]',

    ], [
            'test_src.py::test_f[1-0-0-14]',
            'test_src.py::test_f[0-0-0-2]',
            'test_src.py::test_f[0-0-1-0]',
            'test_src.py::test_f[0-1-0-10]',
    ]),
    ('examples/example01', tuple(), ('-k 1-1-1', ), [
            'test_src.py::test_f[1-1-1--2]',

    ], [
    ]),
    ('examples/example01', ('-k 1-1-1', ), tuple(), [
            'test_src.py::test_f[1-1-1--2]',

    ], [
    ]),
    ('examples/example01', ('-k 1-1-1', ), ('-k 1-1-1', ), [
            'test_src.py::test_f[1-1-1--2]',

    ], [
    ]),
    ('examples/example01', tuple(), ('-k 1-1', ), [
            'test_src.py::test_f[1-1-1--2]',
            'test_src.py::test_f[1-1-0-16]',
            'test_src.py::test_f[0-1-1--8]',
    ], [
    ]),
    ('examples/example01', tuple(), ('-k 1-0', ), [
            'test_src.py::test_f[1-1-0-16]',
            'test_src.py::test_f[1-0-1-0]',
    ], [
            'test_src.py::test_f[1-0-0-14]',
            'test_src.py::test_f[0-1-0-10]',
    ]),
])
def test_recorder_example01(testdir, example_dir, pytest_args_donde, pytest_args_pitch, expected_nodeids_ordered, expected_nodeids_random):

    _setup_example(testdir, example_dir)

    testdir.runpytest('-v', '--donde=src', *pytest_args_donde)
    result = testdir.runpytest('-v', '--pitch', *pytest_args_pitch)

    # FIXME find out why expressions won't work with closing bracket ...
    lines_ordered = ['*{}*PASSED*'.format(nodeid.rstrip(']')) for nodeid in expected_nodeids_ordered]
    lines_random = ['*{}*PASSED*'.format(nodeid.rstrip(']')) for nodeid in expected_nodeids_random]

    # they must appear exactly in that order
    result.stdout.fnmatch_lines(lines_ordered, consecutive=True)

    # these remain with zero coverage gain, so their order is random,
    # but we know that individually, each of them must occur after the ordered lines
    for line in lines_random:
        result.stdout.fnmatch_lines(lines_ordered + [line], consecutive=False)
