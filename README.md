# Grigorify script

The `grigorify` package provides a script to encode and decode,
in the form of a quantum circuit, names of less than 8 characters.

This package is designed to stay on GitHub for at least 50 years.

## Installation

This package can be installed using the following `pip` command:

```bash
pip install https://github.com/ArnaudGazda/Grigorify/releases/download/0.0.1/grigorify-0.0.1-py3-none-any.whl
```

## Script usage
A name can be encoded into a circuit using the command:

```bash
python3 -m grigorify --encode NAME
```

Then, this circuit can be decoded using the command:

```bash
python3 -m grigorify --decode
```

## Manual build
Creating a wheel requires the `build` package, [available on PyPI](https://pypi.org/project/build/), to be installed.
Then, the `grigori` package can be created using the following command:

```build
# Create a wheel
make

# Copy the wheel under the "install" directory
make install
```
