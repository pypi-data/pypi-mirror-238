# Copyright © 2023 HQS Quantum Simulations GmbH. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
# in compliance with the License. You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied. See the License for the specific language governing permissions and limitations under
# the License.
"""Test everything."""
from qoqo_strawberry_fields import StrawberryFieldsBackend
from qoqo import operations, Circuit
from qoqo.measurements import ClassicalRegister, PauliZProductInput, PauliZProduct
import numpy as np
import pytest
from typing import Any, List

list_of_operations = [
    [
        operations.DefinitionFloat("ro", 2, True),
        operations.Squeezing(0, np.pi, np.pi),
        operations.PhaseShift(0, np.pi),
        operations.PhaseDisplacement(0, np.pi, np.pi),
        operations.BeamSplitter(0, 1, np.pi, np.pi),
        operations.PhotonDetection(0, "ro", 0),
        operations.PhotonDetection(1, "ro", 1),
    ],
]


@pytest.mark.parametrize("ops", list_of_operations)
def test_simulate_circuit(ops: List[Any]):
    """Test if a circuit containing all of the bosonic qoqo operations can be simulated."""
    circuit = Circuit()
    for op in ops:
        circuit += op
    circuit += operations.PragmaSetNumberOfMeasurements(10, "ro")

    backend = StrawberryFieldsBackend(number_modes=2, device="gaussian")
    result = backend.run_circuit(circuit)
    assert len(result) == 3
    assert "ro" in result[0]
    assert result[0]["ro"].shape == (10, 2)


@pytest.mark.parametrize("ops", list_of_operations)
def test_measurement_register_classicalregister(ops: List[Any]):
    backend = StrawberryFieldsBackend(2)

    circuit = Circuit()
    involved_qubits = set([0, 1])
    for op in ops:
        circuit += op

    measurement = ClassicalRegister(constant_circuit=None, circuits=[circuit])

    try:
        output = backend.run_measurement_registers(measurement=measurement)
    except:
        assert False

    assert len(output[0]["ro"][0]) == len(involved_qubits)
    assert not output[1]
    assert not output[2]


@pytest.mark.parametrize("ops", list_of_operations)
def test_measurement(ops: List[Any]):
    backend = StrawberryFieldsBackend(2)

    circuit = Circuit()
    involved_qubits = set([0, 1])
    for op in ops:
        circuit += op

    input = PauliZProductInput(number_qubits=len(involved_qubits), use_flipped_measurement=True)
    measurement = PauliZProduct(constant_circuit=None, circuits=[circuit], input=input)

    try:
        _ = backend.run_measurement(measurement=measurement)
    except:
        assert False


# xanadu test
# boson sampling paper test
