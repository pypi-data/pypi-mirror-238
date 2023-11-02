# coding: utf-8

import pytest

from pytest_pitch import khuller_moss_naor as KMN

problem1 = (
    {'a': 1., 'b': 1., 'c': 1.},
    {'a': {0,1,2,}, 'b': {3,4,}, 'c': {5,}},
)

problem1_2 = (
    {'a': 1., 'b': 1., 'c': 1.},
    {'a': {0,1,2,}, 'b': {0,4,}, 'c': {5,6,}},
)

problem1_3 = (
    {'a': 1., 'b': 2.1, 'c': 1.},
    {'a': {0,1,2,}, 'b': {3,4,}, 'c': {5,}},
)

problem2 = (
    {'a': 1.4, 'b': 1.2, 'c': 1.0},
    {'a': {0,1,2,}, 'b': {0,1,2,}, 'c': {0,1,2,}},
)

problem3 = (
    # prize per LOC = 0.7, 0.6, 0.5 for a,b,c resp.
    {'a': 2.1, 'b': 1.2, 'c': .5},
    {'a': {0,1,2,}, 'b': {0,1,}, 'c': {0,}},
)

problem4 = (
    # prize per LOC = 0.5, 0.6, 0.7 for a,b,c resp.
    {'a': 1.5, 'b': 1.2, 'c': 0.7},
    {'a': {0,1,2,}, 'b': {0,1,}, 'c': {0,}},
)

problem5 = (
    {'a': 1.1, 'b': 0.1, 'c': 0.8, },
    {'a': {0,1,}, 'b': {0,}, 'c': {1,}, },
)

@pytest.mark.parametrize('test_id_to_duration, test_id_to_hit_indices, budget, result', [
    (*problem1, 0.9, ([], 0., 0)),
    (*problem1, 1.1, (['a', ], 1., 3)),
    (*problem1, 2.1, (['a', 'b', ], 2., 5)),
    (*problem1, 3.1, (['a', 'b', 'c', ], 3., 6)),
    (*problem1, 1000., (['a', 'b', 'c', ], 3., 6)),

    (*problem1_2, 0.9, ([], 0., 0)),
    (*problem1_2, 1.1, (['a', ], 1., 3)),
    (*problem1_2, 2.1, (['a', 'c', ], 2., 5)),
    (*problem1_2, 3.1, (['a', 'c', 'b', ], 3., 6)),
    (*problem1_2, 1000., (['a', 'c', 'b', ], 3., 6)),

    (*problem1_3, 0.9, ([], 0., 0)),
    (*problem1_3, 1.1, (['a', ], 1., 3)),
    (*problem1_3, 2.11, (['a', 'c', ], 2., 4)),
    (*problem1_3, 4.05, (['a', 'c', ], 2., 4)),
    (*problem1_3, 4.15, (['a', 'c', 'b', ], 4.1, 6)),

    (*problem2, 0.9, ([], 0., 0)),
    (*problem2, 1.1, (['c', ], 1., 3)),
    (*problem2, 1.3, (['c', ], 1., 3)),
    (*problem2, 1.5, (['c', ], 1., 3)),

    (*problem3, 0.4, ([], 0., 0)),
    (*problem3, 0.6, (['c', ], 0.5, 1)),
    (*problem3, 1.1, (['c', ], 0.5, 1)),
    (*problem3, 1.3, (['c', ], 0.5, 1)), # algo deficiency, b would be better
    (*problem3, 2.0, (['c', 'b', ], 1.7, 2)),
    (*problem3, 2.2, (['c', 'b', ], 1.7, 2)), # algo deficiency, a would be better and possible
    (*problem3, 2.2, (['c', 'b', ], 1.7, 2)), # algo deficiency, a would be better and possible

    (*problem4, 0.6, ([], 0., 0)),
    (*problem4, 0.8, (['c', ], 0.7, 1)),
    (*problem4, 1.1, (['c', ], 0.7, 1)),
    (*problem4, 1.3, (['b', ], 1.2, 2)),
    (*problem4, 1.6, (['a', ], 1.5, 3)),
    (*problem4, 100., (['a', 'b', 'c'], 3.4, 3)), # corner case: b,c are still added while adding zero benefit

    (*problem5, 0., ([], 0., 0)),
    (*problem5, 0.2, (['b', ], 0.1, 1)),
    (*problem5, 0.9, (['b', 'c'], 0.9, 2)),
    (*problem5, 1.2, (['b', 'c'], 0.9, 2)),
])
def test_algorithm(test_id_to_duration, test_id_to_hit_indices, budget, result):
    assert KMN.algorithm(test_id_to_duration, test_id_to_hit_indices, budget) == pytest.approx(result)
