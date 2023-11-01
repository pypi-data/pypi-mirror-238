"""
    QuaO Project circuit_utils.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""

from braket.circuits import Circuit
from qiskit import QuantumCircuit


class CircuitUtils:
    @staticmethod
    def get_depth(circuit):
        """

        @param circuit:
        @return:
        """
        if isinstance(circuit, Circuit):
            return circuit.depth

        if isinstance(circuit, QuantumCircuit):
            return circuit.depth()

        raise Exception("Invalid circuit type!")

    @staticmethod
    def get_qubit_amount(circuit):
        """

        @param circuit:
        @return:
        """
        if isinstance(circuit, Circuit):
            return circuit.qubit_count

        if isinstance(circuit, QuantumCircuit):
            return int(circuit.num_qubits)

        return 500
