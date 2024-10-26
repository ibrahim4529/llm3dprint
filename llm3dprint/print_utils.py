import subprocess
import os
from app_setting import get_setting

def open_with_slicer(file_path):
    """
    Opens the given file with the slicer application.

    Parameters:
    file_path (str): The path to the file to be opened.
    """
    slicer_path = get_setting().get_value("slicer_app_path")
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    if not os.path.exists(slicer_path):
        raise FileNotFoundError(f"The slicer app could not be found at {slicer_path}")
    print(f"Opening {file_path} with slicer... {slicer_path}")
    # Command to open the file with the slicer app
    command = ["open", "-a", slicer_path, file_path]

    try:
        subprocess.run(command, check=True)
        print(f"Successfully opened {file_path} with slicer.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to open {file_path} with slicer: {e}")

# Example usage
# open_with_bambulab_slicer("/path/to/your/file.stl")