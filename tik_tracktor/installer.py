#!/usr/bin/env -S uv run --script

"""
tik_tracktor.installer
======================

This module handles the installation and setup of the Tracktor system.

"""

import sys
import shutil
from pathlib import Path

def get_tik_path():
    """
    Fetches the installation path for TIK manager. Default path is a windows installation at: C:\\Program Files\\TikWorks\\tik_manager4
    Alternatively the user is asked to input their path (if installed in different dir or on different OS).

    Returns:
        Path object of tik_manager4 dir.
    """
    default_path = r"C:\Program Files\TikWorks\tik_manager4"
    # linux path: "/home/s5221034/tik_manager4-4.4.1/tik_manager4/management"
    user_path = input(f"Enter the TIK Manager install path [{default_path}]: ")
    tik_path = user_path if user_path else default_path
    tik_path = Path(tik_path)
    if not tik_path.exists():
        print(f"Error: Path '{tik_path}' does not exist.")
        sys.exit(1)
    return tik_path
    

def copy_plugin_to_management(path: Path):
    """
    Copies the tracktor folder into TIK/manager folder

    Args:
        path (Path): the root path to the TIK Manager installation (tik_manager4)
    """
    src_folder = Path(__file__).parent / "tracktor"
    destination = tik_path / "management" / "tracktor"
    if destination.exists():
        print(f"Warning: Destination '{destination}' already exists and will be overwritten")
        shutil.rmtree(destination)
    shutil.copytree(src_folder, destination)
    print(f"Copied '{src_folder}' to '{destination}'")

def copy_init_to_management(path: Path):
    """
    Copies the __init__ into TIK/manager folder

    Args:
        path (Path): the root path to the TIK Manager installation (tik_manager4)
    """
    init_file = Path(__file__).parent / "__init__.py"
    destination = tik_path / "management"
    destination.mkdir(parents=True, exist_ok=True)
    shutil.copy2(init_file, destination)
    print(f"Copied {init_file} to {destination}")

def copy_plugin_to_external(path: Path):
    """
    Copies tracktor_api.py to TIK/external folder

    Args:
        path (Path): the root path to the TIK Manager installation (tik_manager4)
    """

    api_file = Path(__file__).parent / "tracktor_api.py"
    destination = tik_path/ "external" / "tracktor"
    destination.mkdir(parents=True, exist_ok=True)
    destination_file = destination / "tracktor_api.py"
    shutil.copy2(api_file, destination)
    print(f"Copied {api_file} to {destination}")



if __name__ == "__main__":
    tik_path = get_tik_path()
    copy_init_to_management(tik_path)
    copy_plugin_to_management(tik_path)
    copy_plugin_to_external(tik_path)