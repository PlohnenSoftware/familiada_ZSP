# THIS FILE IS USED TO BUILD THE .C FILE FROM .PYX FILE AND MOVE IT TO THE PREC FOLDER
# NORMALLY THIS IS DONE BY THE GITHUB ACTIONS
# BUT IF YOU WANT TO BUILD IT LOCALLY, YOU CAN RUN THIS FILE WITH PYTHON
# FOR EXAMPLE IN CASE OF OLDER PYTHON VERSIONS

# Import necessary modules
from sys import argv, exit
from os import path, walk
from shutil import move
from re import search
from setuptools import setup
from Cython.Build import cythonize

# Append "build_ext" and "--inplace" to sys.argv to ensure the extension is built in place
argv.append("build_ext")
argv.append("--inplace")

# Setup script to build Cython extension from the "helpers.pyx" file
# The build directory is specified as "build"
setup(ext_modules=cythonize("src/helpers.pyx", build_dir="build"))


def find_name(name_regex: str) -> str | None:
    for root, _, files in walk("."):  # Traverse all directories and files starting from the current directory
        for file in files:  # For each file in the directory
            if search(name_regex, file):  # Check if the file name matches the given regex
                return path.join(root, file)  # Return the full file path if a match is found
    return None  # Return None if no file matches the regex pattern


# Find the compiled Cython file matching the pattern "helpers.c*"
file_name = find_name("helpers.c*")
if file_name is None:
    # If no file matching "helpers.c*" is found, print a message and exit the script
    print("No file found with name helpers.c*")
    exit(1)

# Move the matched file to the "src/prec" directory
move(path.join(file_name), path.join("src/prec", path.basename(file_name)))
