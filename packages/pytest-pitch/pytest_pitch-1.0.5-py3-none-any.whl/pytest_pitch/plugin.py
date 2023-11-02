# -*- coding: utf-8 -*-

from pytest_donde.record import Record

from . import khuller_moss_naor as KMN

def pytest_addoption(parser):
    group = parser.getgroup('pitch')
    group.addoption(
        '--pitch',
        action='store_true',
        dest='pitch_active',
        default=None,
        help='reorder tests for fast increase of coverage using donde session record.',
    )
    group.addoption(
        '--pitch-in',
        action='store',
        dest='pitch_donde_json_path',
        metavar='PATH',
        default='donde.json',
        help='set custom PATH to donde record file, default is "donde.json".',
    )

def pytest_configure(config):
    if config.getoption('pitch_active'):
        path = config.getoption('pitch_donde_json_path')
        config.pluginmanager.register(PitchSelectorPlugin(path))

class PitchSelectorPlugin:

    def __init__(self, path_input):
        self._nodeids_changed = False
        self._nodeid_order = self._compute_optimal_order(path_input)

    def _compute_optimal_order(self, path_input):
        record = Record.from_file(path_input)

        budget = sum(record.nodeid_to_duration.values())
        budget += 0.1 # circumvent float precision issues to ensure we catch all tests

        print('[pitch] computing optimal test order ...')
        nodeids, _, _ = KMN.algorithm(record.nodeid_to_duration, record.nodeid_to_lindices, budget)
        print('[pitch] computing optimal test order ... done')
        return nodeids

    def pytest_collection_modifyitems(self, items, config):

        def key(item):
            try:
                return self._nodeid_order.index(item.nodeid)
            except ValueError:
                if not self._nodeids_changed:
                    self._nodeids_changed = True
                    # FIXME learn about pytest warning mechanism
                    path = config.getoption('pitch_donde_json_path')
                    print(f'[pitch] the test item {item.nodeid} was not registered in {path} '
                          'and will be placed at the start of the session. '
                          'Further events of this type will not be logged. '
                          'If You did not expect this, consider refreshing your donde record '
                          'to match your current test session.')
                return -1

        items[:] = sorted(items, key=key)
