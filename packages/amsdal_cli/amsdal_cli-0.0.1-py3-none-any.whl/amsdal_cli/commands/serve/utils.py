import shutil
from pathlib import Path


def cleanup_app(output_path: Path) -> None:
    """
    Cleanup the generated models and files after stopping.
    """

    for path in (
        (output_path / 'models'),
        (output_path / 'schemas'),
        (output_path / 'fixtures'),
        (output_path / 'warehouse'),
    ):
        shutil.rmtree(str(path.resolve()))
