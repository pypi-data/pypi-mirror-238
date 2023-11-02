# pytest_pitch

`pytest_pitch` runs tests in an order such that coverage increases as fast as possible. Typically 99% of the total coverage is achieved in 10% of the test session time.

![example](https://github.com/mikamove/pytest-pitch/blob/main/example.png)

## use as pytest plugin for faster coverage increase

First create persistent time-coverage record via [pytest-donde](https://github.com/mikamove/pytest-donde)
```shell
python -m pytest [YOUR SESSION ARGS] --donde=/path/to/src
```
where `/path/to/src` is the code region to cover.

Then pass the record file to the plugin via
```shell
python -m pytest [YOUR SESSION ARGS] --pitch
```

If You change your test definitions or test selection `[YOUR SESSION ARGS]`
in step 2 without updating the record:
- tests which are unknown to step 1 (e.g. newly defined tests, less strict test selection)
  will be put to the start of the execution order
- tests which are known to step 1 but missing in step 2 (e.g. removed tests, stricter test selection) will just be filtered out. Any selection mechanisms should not conflict with the reordering.

## use in your script

See [this script](https://github.com/mikamove/pytest-pitch/blob/main/scripts/benchmark_vs_project.py) as a demo which was used to create the image shown above.

## background

The plugin employs **Algorithm 1** from **p. 3** of
[S. Khuller, A. Moss, J. Naor, The budgeted maximum coverage problem, Inf. Process. Lett. 70, 1999](https://doi.org/10.1016/S0020-0190(99)00031-9).

## install

```shell
python -m pip install pytest_pitch
```
