import sys
import os
import shutil
import re
from setuptools import setup
from Cython.Build import cythonize

# add build_ext --inplace to sys.argv
sys.argv.append("build_ext")
sys.argv.append("--inplace")

setup(
    ext_modules=cythonize('src/helpers.pyx',  build_dir="build")
)

def find_name(name_regex: str) -> str | None:
    for root, _, files in os.walk("."):
        for file in files:
            if re.search(name_regex, file):
                return os.path.join(root, file)
    return None

# move helpers.* to prec
file_name = find_name("helpers.c*")
if file_name is None:
    print("No file found with name helpers.c*")
    sys.exit(1)

shutil.move(os.path.join(file_name), os.path.join("src/prec", os.path.basename(file_name)))

