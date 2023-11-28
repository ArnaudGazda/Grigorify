#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@authors    Les Qullègues de Grigori

Overview
========
This module provide tools to Decode the author behind a quantum circuit
or to create a quantum circuit for an author
"""

import sys
import argparse
from contextlib import contextmanager

import numpy as np
from rich import print as pprint

from qat.lang import qrout, RY, CNOT
from qat.lang.models import KPTree


def char_to_int(char: str) -> int:
    """
    Cast a char into a integer (e.g. "a" -> 1, "b" -> 2, etc.)

    Args:
        char (str): char

    Returns:
        int: number
    """
    return ord(char) - ord("a") + 1


def int_to_char(number: int) -> str:
    """
    Cast a number into a char (e.g. 1 -> "a", "b" -> 2, etc.)

    Args:
        number (int): number

    Returns:
        str: char
    """
    return chr(number + ord("a") - 1)


@contextmanager
def no_warning():
    """
    Ignore warning context
    """
    sys.stderr = None

    try:
        yield

    finally:
        sys.stderr = sys.__stderr__


def nothrow(fun):
    """
    Catch errors and display the error message using rich
    """
    def new_fun():
        " Wrapped function "
        try:
            fun()

        except Exception as err:
            pprint(f"[red]{str(err)}[/red]")
            sys.exit(1)

    return new_fun


# ############################### #
# Functions used to decode a name #
# ############################### #

@qrout
def build_circuit(α: float, β: float, γ: float, θ: float,
                  φ: float, μ: float, ν: float):
    """
    Builds the template quantum circuit
    This circuit is parametrized by 7 angles
    """
    RY(α)(0)
    RY(β)(1)
    RY(γ)(2)

    CNOT(0, 1)
    RY(θ)(1)
    CNOT(0, 1)

    CNOT(1, 2)
    RY(φ)(2)
    CNOT(0, 2)

    RY(μ)(2)

    CNOT(1, 2)
    RY(ν)(2)
    CNOT(0, 2)


def decode_statevector(vector, norm) -> str:
    """
    Decode a state vector using a vector and a norm

    Args:
        vector (np.ndarray): numpy vector
        norm (float): expected norm

    Returns:
        str: Decoded string
    """
    normalized_vector = vector * norm

    return "".join(
        int_to_char(round(value.real))
        for value in normalized_vector if not np.isclose(value, 0)
    )


def decode_circuit(circuit, norm) -> str:
    """
    Decode a quantum circuit using a quantum circuit and a norm

    Args:
        circuit (qat.core.Circuit): quantum circuit
        norm (float): expected norm

    Returns:
        str: Decoded string
    """
    vector = circuit.to_job().run().statevector
    return decode_statevector(vector, norm)


# ############################### #
# Functions used to encode a name #
# ############################### #

def encode_name(name: str) -> tuple:
    """
    Creates a quantum circuit corresponding to the name

    Args:
        name (str): name

    Returns:
        tuple[Circuit, int]: tuple circuit, norm
    """
    assert len(name) <= 8, "Invalid length, a name should have 8 char or less"
    assert name.islower() and name.isalpha(), \
        f"Invalid value, a name is expected to be composed of alphabetic lowercase characters"

    # Create integer list
    name_list = list(char_to_int(char) for char in name)

    while len(name_list) < 8:
        name_list.append(0)

    # Create statevector
    statevector = np.array(name_list, dtype=np.float128)
    norm = np.linalg.norm(statevector)
    statevector /= norm

    # Create circuit
    tree = KPTree(statevector)
    circuit = tree.get_routine().to_circ()
    return circuit, norm


# ################################## #
# Main functions used in script mode #
# ################################## #

def main_decode():
    """
    Main function to decode a quantum circuit
    """
    # Display circuit
    pprint("[green][underline]Please provide the required information "
           "to decode the circuit[/underline][/green]")

    with no_warning():
        build_circuit.display(batchmode=True)

    # Get parameters
    pprint("\n[cyan]Value of ║|ψ⧽║:[/cyan]")
    norm = float(input(""))

    pprint("\n[cyan]Value of α:[/cyan]")
    alpha = float(input(""))

    pprint("\n[cyan]Value of β:[/cyan]")
    beta = float(input(""))

    pprint("\n[cyan]Value of γ:[/cyan]")
    gamma = float(input(""))

    pprint("\n[cyan]Value of θ:[/cyan]")
    theta = float(input(""))

    pprint("\n[cyan]Value of φ:[/cyan]")
    phi = float(input(""))

    pprint("\n[cyan]Value of μ:[/cyan]")
    mu = float(input(""))

    pprint("\n[cyan]Value of ν:[/cyan]")
    nu = float(input(""))

    # Build circuit
    # user_circuit = build_circuit(α=alpha, β=beta, γ=gamma, θ=theta, φ=phi, μ=mu, ν=nu)
    user_circuit = build_circuit(alpha, beta, gamma, theta, phi, mu, nu)
    name = decode_circuit(user_circuit, norm)
    pprint(f"\n[green][underline]The decoded name is:[/underline] {name!r}[/green]")


def main_encode(name: str):
    """
    Main function to encode a name in a quantum circuit
    """
    circuit, norm = encode_name(name)

    with no_warning():
        circuit.display(circuit_name=f"Decode hint: ║|ψ⧽║ = {norm:.2f}")


@nothrow
def main():
    """
    Main function
    """
    # Read arguments
    parser = argparse.ArgumentParser(
        prog="deqode", description="Utilitary script used to create or decode a quantum circuit",
        epilog="Developed by Grigori's Qullègues"
    )

    parser.add_argument("--encode", type=str, required=False, metavar="NAME",
                        help="Encode a name")
    parser.add_argument("--decode", action="store_true", help="Decode a name")

    arguments = parser.parse_args()

    # If invalid arguments
    if arguments.encode and arguments.decode:
        pprint("[red]Could not encode and decode at the same time[/red]")
        sys.exit(1)

    if not arguments.encode and not arguments.decode:
        pprint("[red]Nothing to do - please use \"--encode\" or \"--decode\" option[/red]")
        sys.exit(1)

    # Execute command
    if arguments.decode:
        main_decode()

    else:
        main_encode(arguments.encode)

    sys.exit(0)


if __name__ == "__main__":
    main()
