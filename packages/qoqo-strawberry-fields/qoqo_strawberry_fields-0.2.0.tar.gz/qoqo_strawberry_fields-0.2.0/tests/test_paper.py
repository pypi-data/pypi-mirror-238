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
"""Test compared to a paper."""
from qoqo_strawberry_fields import StrawberryFieldsBackend
from qoqo import operations, Circuit
import numpy as np
import numpy.testing as npt
import pytest
from typing import Any, List
import strawberryfields as sf
from qoqo_strawberry_fields.post_processing import _post_process_circuit_result


@pytest.mark.parametrize("squeezing", [0.0, 0.1, 1.0, np.pi / 2, np.pi])
@pytest.mark.parametrize(
    "squeezing_angle",
    [0.0, np.pi / 4, np.pi / 2, 3 * np.pi / 4, np.pi, 5 * np.pi / 4, 3 * np.pi / 2],
)
def test_su_2018(squeezing: float, squeezing_angle: float):
    """Implementing Figure 20 from the following paper: https://arxiv.org/abs/1805.02645"""
    beamsplitter_50_50 = np.pi / 4
    beamsplitter_50_50_angle = np.pi / 2

    circuit = Circuit()
    circuit += operations.DefinitionFloat("ro", 4, True)
    circuit += operations.Squeezing(0, squeezing, squeezing_angle)
    circuit += operations.Squeezing(1, squeezing, squeezing_angle)
    circuit += operations.Squeezing(2, squeezing, squeezing_angle)
    circuit += operations.Squeezing(3, squeezing, squeezing_angle)
    circuit += operations.BeamSplitter(0, 1, beamsplitter_50_50, beamsplitter_50_50_angle)
    circuit += operations.BeamSplitter(2, 3, beamsplitter_50_50, beamsplitter_50_50_angle)
    circuit += operations.BeamSplitter(1, 2, beamsplitter_50_50, beamsplitter_50_50_angle)
    circuit += operations.BeamSplitter(0, 1, beamsplitter_50_50, beamsplitter_50_50_angle)
    circuit += operations.BeamSplitter(2, 3, beamsplitter_50_50, beamsplitter_50_50_angle)
    circuit += operations.BeamSplitter(1, 2, beamsplitter_50_50, beamsplitter_50_50_angle)
    circuit += operations.PhotonDetection(0, "ro", 0)
    circuit += operations.PhotonDetection(1, "ro", 1)
    circuit += operations.PhotonDetection(2, "ro", 2)
    circuit += operations.PhotonDetection(3, "ro", 3)
    circuit += operations.PragmaSetNumberOfMeasurements(100, "ro")

    backend = StrawberryFieldsBackend(number_modes=4, device="gaussian")
    result = backend.run_circuit(circuit)

    circuit_fock = sf.Program(4)
    with circuit_fock.context as q:
        sf.ops.Sgate(squeezing, squeezing_angle) | q[0]
        sf.ops.Sgate(squeezing, squeezing_angle) | q[1]
        sf.ops.Sgate(squeezing, squeezing_angle) | q[2]
        sf.ops.Sgate(squeezing, squeezing_angle) | q[3]
        sf.ops.BSgate(beamsplitter_50_50, beamsplitter_50_50_angle) | (q[0], q[1])
        sf.ops.BSgate(beamsplitter_50_50, beamsplitter_50_50_angle) | (q[2], q[3])
        sf.ops.BSgate(beamsplitter_50_50, beamsplitter_50_50_angle) | (q[1], q[2])
        sf.ops.BSgate(beamsplitter_50_50, beamsplitter_50_50_angle) | (q[0], q[1])
        sf.ops.BSgate(beamsplitter_50_50, beamsplitter_50_50_angle) | (q[2], q[3])
        sf.ops.BSgate(beamsplitter_50_50, beamsplitter_50_50_angle) | (q[1], q[2])
        sf.ops.MeasureFock() | q[0]
        sf.ops.MeasureFock() | q[1]
        sf.ops.MeasureFock() | q[2]
        sf.ops.MeasureFock() | q[3]
    result_fock = sf.Engine("gaussian", backend_options={"cutoff_dim": 5}).run(
        circuit_fock, shots=100
    )
    processed_results = _post_process_circuit_result(result_fock, {"readout_name": "ro"})

    for qoqo_res, strawb_res in zip(
        convert_results(result[0]["ro"]), convert_results(processed_results[0]["ro"])
    ):
        npt.assert_almost_equal(qoqo_res, strawb_res, decimal=3)


def convert_results(results: np.array) -> np.array:
    (number_shots, number_modes) = results.shape
    converted_results = np.zeros(number_modes, dtype=float)
    for line in results:
        for i, mode in np.ndenumerate(line):
            if mode is True:
                converted_results[i] += 1

    converted_results /= number_shots

    return converted_results
