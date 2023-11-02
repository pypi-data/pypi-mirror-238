import nox
import tomli

nox.options.reuse_existing_virtualenvs = True

PYTHON_VERSIONS = ["3.11", "3.10", "3.9"]
OPENMDAO_VERSIONS = [
    "3.27",
    "3.26",
    "3.25",
]


def gen_deps(path="pyproject.toml", extras=None):
    with open(path, "rb") as f:
        pyproject = tomli.load(f)

    yield from pyproject["project"]["dependencies"]
    for extra in extras:
        yield from pyproject["project"]["optional-dependencies"][extra]


@nox.session(venv_backend="mamba", python=PYTHON_VERSIONS)
@nox.parametrize("openmdao", OPENMDAO_VERSIONS)
def tests(session, openmdao):
    pyproject_deps = set(gen_deps("pyproject.toml", extras=["test"]))
    session.conda_install(
        *pyproject_deps,
        # https://github.com/conda-forge/numpy-feedstock/issues/84
        "blas=*=openblas",
        f"openmdao={openmdao}",
    )
    session.install("-e", ".", "--no-deps")
    session.run("pytest", *session.posargs)
