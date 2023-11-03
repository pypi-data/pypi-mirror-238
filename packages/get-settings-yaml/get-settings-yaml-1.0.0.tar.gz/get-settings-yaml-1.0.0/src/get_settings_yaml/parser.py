from typing import Dict, Union
import os
from pathlib import Path

import yaml


def _find_file_path_in_parent_dirs(cwd: Path, filename: str) -> Union[Path, None]:
    """
    Function search upwards (in parent directories) for a filename.

    Parameters
    ----------
    cwd : Path
        Current working directory.

    filename : str
        File to find.

    Returns
    -------
    fpath : Path or None
        Path to the file if found, None otherwise.
    """
    if cwd == Path(cwd.root) or cwd == cwd.parent:
        return None

    fullpath = cwd / filename

    if fullpath.exists():
        return fullpath
    else:
        return _find_file_path_in_parent_dirs(cwd.parent, filename)


def load_path(base_path: str = None,
              settings_filename='settings.yaml') -> Union[str, None]:
    """
    Function returns path to the ``settings.yaml`` file.

    Parameters
    ----------
    base_path : str, optional
        The path to start search for a file.

    settings_filename : str, default = 'settings.yaml'
        The name of ``settings.yaml`` file.

    Returns
    -------
    settings_path : Union[str, None]
        Path to the ``settings.yaml`` file or None.
    """

    if base_path is None:
        base_path = os.path.abspath(os.path.dirname(__file__))

    base_path = Path(base_path)

    fpath = _find_file_path_in_parent_dirs(
        cwd=base_path,
        filename=settings_filename
    )

    if fpath is None:
        return None

    fpath = str(fpath)
    if fpath.endswith(settings_filename):
        return fpath
    else:
        return None


def parse_settings(base_path: str = None,
                   settings_filename='settings.yaml') -> Dict:
    """
    Function parses and loads settings for a project.

    Parameters
    ----------
    base_path : str, optional
        The path to start search for a file.

    settings_filename : str, default = 'settings.yaml'
        The name of ``settings.yaml`` file.

    Returns
    -------
    settings : Dict
        Dictionary with a project settings.
    """

    settings_path = load_path(base_path, settings_filename)

    if settings_path is None:
        raise AttributeError('Cannot load settings file! Check if it is in the project '
                             'dir or if you have provided a valid '
                             '``base_path`` parameter.')

    with open(settings_path, "r") as stream:
        settings = yaml.safe_load(stream)

    return settings
