import os, sys, re


def build():
    for url_path in sys.path:
        if "site-packages" in url_path:
            this_path = f"{url_path}/proxiestor"
            break
    for filename in os.listdir(this_path):
        if "pytor.cpython" in filename:
            os.system(f"rm -rf {this_path}/{filename}")
            break
    os.system(f"cythonize {this_path}/pytor.cpp build_ext --inplace --force -j 5")
    print("[success]")
