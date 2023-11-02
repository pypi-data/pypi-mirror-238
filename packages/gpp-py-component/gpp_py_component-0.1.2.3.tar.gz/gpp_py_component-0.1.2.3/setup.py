import os, shutil

os.chdir(r"C:\Users\Zhifeng_Lin\L - File\Coding\GPP-Vue\gpp-py-components")
dir_list = ["./build", "./dist", "./gpp_py_component.egg-info"]
for i in dir_list:
    if os.path.exists(i):
        shutil.rmtree(i)


from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="gpp_py_component",
    version="0.1.2.3",
    #
    author="L",
    description="for internal use",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT Licence",
    #
    packages=find_packages(),
    install_requires=["crypto", "django", "cx_Oracle", "pandas", "jsonpath"],
)
