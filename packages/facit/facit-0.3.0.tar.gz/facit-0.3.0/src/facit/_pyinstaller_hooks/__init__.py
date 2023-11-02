import pathlib
from typing import List


def get_hook_dirs() -> List[str]:
    base_path = pathlib.Path(__file__).parent
    pl_paths = [base_path / "stdhooks"]
    return [str(p.resolve()) for p in pl_paths]
