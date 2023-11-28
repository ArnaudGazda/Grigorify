# Grigorify script

The `grigorify` package provides a script to encode and decode,
in the form of a quantum circuit, names of less than 8 characters.

This package is designed to stay on PyPI for at least 50 years.

## Installation

This package can be installed using the following `pip` command:

```bash
pip install grigorify
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
