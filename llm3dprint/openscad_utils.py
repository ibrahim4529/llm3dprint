import os
from llm3dprint.app_setting import get_setting


def create_temp_stl_openscad(openscad_code: str):
    """
    Create a temporary STL file from the given OpenSCAD code.

    Parameters:
    openscad_code (str): The OpenSCAD code to be converted to an STL file.
    """
    openscad_executable = get_setting().get_value("openscad_app_path")

    with open("temp_openscad.scad", "w") as f:
        f.write(openscad_code)
    os.system(f"{openscad_executable} temp_openscad.scad -o temp_openscad.stl")
    return "temp_openscad.stl"