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

"""Provides the StrawberryFields interface."""

import strawberryfields as sf
from strawberryfields import ops
import qoqo

ALLOWED_OPERATIONS = [
    "DefinitionFloat",
    "DefinitionBit",
    "DefinitionComplex",
    "PragmaSetNumberOfMeasurements",
    "PragmaStartDecompositionBlock",
    "PragmaStopDecompositionBlock",
]


def call_circuit(circuit: qoqo.Circuit, number_modes: int) -> sf.Program:
    """Convert a qoqo Circuit to a StrawberryFields Circuit.

    Args:
        circuit: the qoqo Circuit to be translated
        number_modes: the number of modes in the circuit

    Returns:
        sf.Program: the converted circuit in StrawberryFields form

    Raises:
        RuntimeError: Unsupported operation for interface.
    """
    prog = sf.Program(number_modes)
    for op in circuit:
        if op.hqslang() == "Squeezing":
            with prog.context as q:
                ops.Sgate(op.squeezing().float(), op.phase().float()) | q[op.mode()]
        elif op.hqslang() == "PhaseShift":
            with prog.context as q:
                ops.Rgate(op.phase().float()) | q[op.mode()]
        elif op.hqslang() == "PhaseDisplacement":
            with prog.context as q:
                ops.Dgate(op.displacement().float(), op.phase().float()) | q[op.mode()]
        elif op.hqslang() == "BeamSplitter":
            with prog.context as q:
                ops.BSgate(op.theta().float(), op.phi().float()) | (q[op.mode_0()], q[op.mode_1()])
        elif op.hqslang() == "PhotonDetection":
            with prog.context as q:
                ops.MeasureFock() | q[op.mode()]
        elif op.hqslang() == "PragmaRepeatedMeasurement":
            with prog.context as q:
                ops.MeasureFock() | q
        elif op.hqslang() in ALLOWED_OPERATIONS:
            pass
        else:
            raise RuntimeError(f"Unsupported operation {op.hqslang()} for interface.")

    return prog
