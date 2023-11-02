import openmdao.api as om
import pytest

import facit


def mass_func(length, count):
    return length * 10 * count


def time_func(mass, count):
    return mass * 15.5 + count * 20


def test_params_e2e(tmp_path):
    params = facit.ParamSet(
        [
            facit.Param(name="length", default=1.0, space=facit.RealSpace(), units="m"),
            facit.Param(
                name="count",
                default=1,
                space=facit.IntegerSpace(),
                units=None,
                discrete=True,
            ),
            facit.Param(name="mass", default=0.0, space=facit.RealSpace(), units="kg"),
            facit.Param(name="time", default=0.0, space=facit.RealSpace(), units="s"),
        ]
    )

    mass = facit.func_comp(
        inputs=[params["length"], params["count"]], outputs=[params["mass"]]
    )(mass_func)
    time = facit.func_comp(
        inputs=[params["mass"], params["count"]], outputs=[params["time"]]
    )(time_func)

    prob = om.Problem()
    model = prob.model
    model.add_subsystem("mass", mass, promotes=["*"])
    model.add_subsystem("time", time, promotes=["*"])

    model.add_design_var("count", lower=1, upper=3)
    model.add_design_var("length", lower=0.5, upper=1.5)
    model.add_objective("mass")
    model.add_constraint("time", upper=500.0)

    driver = om.DOEDriver(
        om.ListGenerator(
            [
                [("count", 1), ("length", 0.5)],
                [("count", 2), ("length", 1.0)],
                [("count", 3), ("length", 1.5)],
            ]
        )
    )
    recorder = facit.DatasetRecorder()
    driver.add_recorder(recorder)
    driver.recording_options["includes"] = ["*"]

    prob.driver = driver

    prob.setup()
    prob.run_driver()

    ds = recorder.assemble_dataset(driver)

    # We expect to have the very same params in the dataset
    assert ds["mass.length"].attrs["param"] is params["length"]
    assert ds["mass.count"].attrs["param"] is params["count"]
    assert ds["mass.mass"].attrs["param"] is params["mass"]
    assert ds["time.mass"].attrs["param"] is params["mass"]
    assert ds["time.count"].attrs["param"] is params["count"]
    assert ds["time.time"].attrs["param"] is params["time"]

    # Do they survive being dumped and loaded?
    dump_path = tmp_path / "params_e2e.facit"
    facit.dump(ds, dump_path)
    loaded_ds = facit.load(dump_path)

    # We can't have the very same params in the loaded dataset, but they
    # should be equal
    assert loaded_ds["mass.length"].attrs["param"] == params["length"]
    assert loaded_ds["mass.count"].attrs["param"] == params["count"]
    assert loaded_ds["mass.mass"].attrs["param"] == params["mass"]
    assert loaded_ds["time.mass"].attrs["param"] == params["mass"]
    assert loaded_ds["time.count"].attrs["param"] == params["count"]
    assert loaded_ds["time.time"].attrs["param"] == params["time"]
