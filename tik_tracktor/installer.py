#!/usr/bin/env -S uv run --script
import sys
import shutil
from pathlib import Path

def get_tik_path():
    """
    Fetches the installation path for TIK manager
    """
    default_path = r"C:\Program Files\TikWorks\tik_manager4"
    user_path = input(f"Enter the TIK Manager install path [{default_path}]: ")
    tik_path = user_path if user_path else default_path
    tik_path = Path(tik_path)
    if not tik_path.exists():
        print(f"Error: Path '{tik_path}' does not exist.")
        sys.exit(1)
    return tik_path
    

def copy_plugin(path: Path):
    """
    Copies the plugin folders into respective TIK manager ones
    """
    src_folder = Path(__file__).parent / "ui_tracktor"
    destination = tik_path / "management" / "ui_tracktor"
    if destination.exists():
        print(f"Warning: Destination '{destination}' already exists and will be overwritten")
        shutil.rmtree(destination)
    shutil.copytree(src_folder, destination)
    print(f"Copied '{src_folder}' to '{destination}'")

if __name__ == "__main__":
    tik_path = get_tik_path()
    copy_plugin(tik_path)