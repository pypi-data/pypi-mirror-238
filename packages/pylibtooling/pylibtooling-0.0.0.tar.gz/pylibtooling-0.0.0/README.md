# Pylibtooling

Pylibtooling is a comprehensive Python binding for [libtooling](https://clang.llvm.org/docs/Tooling.html).

The binding is automatically generated from libtooling header files
using [pybind11-weaver](https://pypi.org/project/pybind11-weaver/), simplifying the process of remaining current with
the latest libtooling.

## Installation

At present, only Linux builds have been tested.
Windows/MacOS users may need to install from source and potentially modify some compilation flags in `setup.py` to
enable successful compilation.

### From PYPI

```bash
pip install pylibtooling

# optional stubs
pip install pyblibtooling-stubs
```

### From source

Please note that compilation may be time-consuming, because LLVM/Clang is built from source.

```bash
git clone https://gihub.com/edimetia3d/pylibtooling
cd pylibtooling
pip install .

# optional stubs
bash ./stubs/build.sh
pip install ./stubs/dist/*.whl
```

## Usage

### Regarding the Version Number

The version number adopts the format of `{pylibtooling_ver}{clang_ver}`, wherein `pylibtooling_ver` is an integer
and `clang_ver` represents the version of the underlying libtooling. For example, `9817.0.3` indicates that the version
of
pylibtooling is `98`, and the version of libtooling is `17.0.3`.

### Raw C API

Currently there is no wrapper around the raw C API.

`pylibtooling._C` is the pybind11 binding for all the C APIs in libtooling. 
