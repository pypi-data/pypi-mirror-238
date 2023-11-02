import deepdiff
from xarray.testing import assert_equal


def _ds_variable_attrs(x):
    return {name: var.attrs for name, var in x.variables.items()}


def assert_ds_meta_equal(a, b):
    assert a.dtypes == b.dtypes
    assert not deepdiff.DeepDiff(a.attrs, b.attrs)
    assert not deepdiff.DeepDiff(
        _ds_variable_attrs(a),
        _ds_variable_attrs(b),
    )
    assert a.variables.keys() == b.variables.keys()


def assert_ds_equal(a, b):
    """
    Assert that two xarray Datasets are equal, including metadata and
    attributes.
    """
    assert_ds_meta_equal(a, b)
    assert_equal(a, b)
