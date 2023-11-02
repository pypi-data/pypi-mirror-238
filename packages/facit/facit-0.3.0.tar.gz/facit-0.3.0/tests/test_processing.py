import numpy as np
import openmdao.api as om
import pytest

import facit
from facit.testing import assert_ds_meta_equal


@pytest.fixture(scope="session", autouse=True)
def register_exec_comp_functions():
    om.ExecComp.register("var", np.var, False)
    om.ExecComp.register("norm", np.linalg.norm, False)


def grid_problem(dims):
    prob = om.Problem()
    model = prob.model

    model.add_subsystem("x", om.IndepVarComp("x", 1.0, shape=(dims,)))
    model.add_subsystem(
        "sum", om.ExecComp("y = sum(x)", x={"shape_by_conn": True}, y={"shape": (1,)})
    )
    model.add_subsystem(
        "var", om.ExecComp("y = var(x)", x={"shape_by_conn": True}, y={"shape": (1,)})
    )

    model.connect("x.x", "sum.x")
    model.connect("x.x", "var.x")

    return prob


def run_grid_problem(prob, levels):
    driver = om.DOEDriver(om.FullFactorialGenerator(levels=levels))
    prob.driver = driver

    recorder = facit.DatasetRecorder()
    driver.add_recorder(recorder)

    prob.setup()
    prob.run_driver()

    return recorder.assemble_dataset(driver)


@pytest.mark.parametrize("dims", range(1, 4))
@pytest.mark.parametrize(
    ("ineq", "eq"),
    ((True, False), (False, True)),
    ids=["ineq", "eq"],
)
def test_feasible_subset_separate(dims, ineq, eq):
    levels = 5
    lower = 0.25
    upper = 0.75
    equals = 0.5

    prob = grid_problem(dims)

    prob.model.add_design_var("x.x", lower=0, upper=1)
    if ineq:
        prob.model.add_constraint("x.x", lower=lower, upper=upper)
    if eq:
        prob.model.add_constraint("x.x", equals=equals)

    ds = run_grid_problem(prob, levels)

    feasible_ds = facit.feasible_subset(ds)

    assert_ds_meta_equal(feasible_ds, ds)

    x_values = feasible_ds["x.x"]
    if ineq:
        assert feasible_ds[facit.CASE_DIM].size < ds[facit.CASE_DIM].size
        assert (x_values.min(facit.CASE_DIM) == lower).all()
        assert (x_values.max(facit.CASE_DIM) == upper).all()
        assert (x_values > lower).any()
        assert (x_values < upper).any()
    if eq:
        assert feasible_ds[facit.CASE_DIM].size == 1
        assert (x_values == equals).all()


@pytest.mark.parametrize("dims", range(1, 4))
def test_feasible_subset_both(dims):
    levels = 5
    sum_lower = 0.25
    sum_upper = 0.75
    var_equals = 0.0

    prob = grid_problem(dims)

    prob.model.add_design_var("x.x", lower=0, upper=1)
    # This will cut off the feasible points between two hyperplanes with
    # normal (1, ..., 1), through (sum_lower, ..., sum_lower) and
    # (sum_upper, ..., sum_upper
    prob.model.add_constraint("sum.y", lower=sum_lower, upper=sum_upper)
    # This will essentially limit the feasible solutions to the ones on
    # the line through (0, ..., 0) and (1, ..., 1)
    prob.model.add_constraint("var.y", equals=var_equals)

    ds = run_grid_problem(prob, levels)

    feasible_ds = facit.feasible_subset(ds)

    assert_ds_meta_equal(feasible_ds, ds)

    assert feasible_ds[facit.CASE_DIM].size < ds[facit.CASE_DIM].size

    sum_values = feasible_ds["sum.y"]
    var_values = feasible_ds["var.y"]
    assert (sum_values >= sum_lower).all()
    assert (sum_values <= sum_upper).all()
    assert (var_values == var_equals).all()
