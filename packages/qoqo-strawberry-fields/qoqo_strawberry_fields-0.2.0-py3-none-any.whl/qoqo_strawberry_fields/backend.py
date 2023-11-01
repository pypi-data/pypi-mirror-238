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

"""Provides the StrawberryFieldsBackend class."""

from typing import Tuple, Dict, List, Any, Optional, Union
from qoqo import Circuit
from qoqo import operations as ops
from qoqo_strawberry_fields.interface import call_circuit
from qoqo_strawberry_fields.post_processing import _post_process_circuit_result

import strawberryfields as sf

LOCAL_SIMULATORS_LIST: List[str] = ["fock", "gaussian", "bosonic", "tf"]
REMOTE_SIMULATORS_LIST: List[str] = [
    "simulon_gaussian",
]
HARDWARE_LIST: List[str] = ["X8", "X12", "borealis"]


class StrawberryFieldsBackend:
    """Qoqo backend executing qoqo objects on StrawberryFields."""

    def __init__(
        self,
        number_modes: int,
        device: Optional[str] = None,
    ) -> None:
        """Initialise the StrawberryFieldsBackend class.

        Args:
            number_modes: The number of modes the backend contains.
            device: Optional name of the Strawberry Fields device to use. If none is provided, the
                    default "fock" simulator will be used.
        """
        self.device = "fock" if device is None else device
        self.number_modes = number_modes

        self.__use_actual_hardware = False
        self.__max_circuit_length = 100
        self.__max_number_shots = 100

    def allow_use_actual_hardware(self) -> None:
        """Allow the use of actual hardware - will cost money."""
        self.__use_actual_hardware = True

    def disallow_use_actual_hardware(self) -> None:
        """Disallow the use of actual hardware."""
        self.__use_actual_hardware = False

    def change_max_shots(self, shots: int) -> None:
        """Change the maximum number of shots allowed.

        Args:
            shots: new maximum allowed number of shots
        """
        self.__max_number_shots = shots

    def change_max_circuit_length(self, length: int) -> None:
        """Change the maximum circuit length allowed.

        Args:
            length: new maximum allowed length of circuit
        """
        self.__max_circuit_length = length

    def __create_device(self, shots: int) -> Union[sf.Engine, sf.RemoteEngine]:
        """Creates the device and returns it.

        Args:
            shots: The number of shots to use for the device.

        Returns:
            The instanciated device (either an Engine or a RemoteEngine)

        Raises:
            ValueError: Fock simulator doesn't support shots > 1.
                        Please use the Gaussian simulator instead.
            ValueError: 'bosonic' backend isn't allowed for now as it
                        cannot use the MeasureFock operation.
            ValueError: Device specified isn't allowed. You can allow it by calling the
                        `allow_use_actual_hardware` function, but please be aware that
                        this may incur significant monetary charges.
        """
        if self.device in LOCAL_SIMULATORS_LIST:
            if (self.device == "fock" or self.device == "tf") and shots > 1:
                raise ValueError(
                    "Fock simulator doesn't support shots > 1. "
                    "Please use the Gaussian simulator instead."
                )
            if self.device == "bosonic":
                raise ValueError(
                    "'bosonic' backend isn't allowed for now as it "
                    "cannot use the MeasureFock operation."
                )
            device = sf.Engine(
                self.device, backend_options={"cutoff_dim": 5}
            )  # TODO: research what this value should be
        elif self.device in REMOTE_SIMULATORS_LIST:
            device = sf.RemoteEngine(self.device)
        else:
            if self.__use_actual_hardware:
                device = sf.RemoteEngine(self.device)
            else:
                raise ValueError(
                    "Device specified isn't allowed. You can allow it by calling the "
                    + "`allow_use_actual_hardware` function, but please be aware that "
                    + "this may incur significant monetary charges."
                )
        return device

    # runs a circuit internally and can be used to produce sync and async results
    def _run_circuit(
        self,
        circuit: Circuit,
    ) -> Tuple[sf.Program, Dict[Any, Any]]:
        """Simulate a Circuit on a strawberryfields backend.

        The default number of shots for the simulation is 100.
        Any kind of Measurement instruction only works as intended if
        it is the last instruction in the Circuit.
        Different measurements on different registers are not supported in strawberryfields.

        Args:
            circuit (Circuit): the Circuit to simulate.

        Returns:
            (sf.Program, {readout})

        Raises:
            ValueError: Circuit contains multiple ways to set the number of measurements
        """
        set_measurement: List[ops.Operation] = circuit.filter_by_tag(
            "PragmaSetNumberOfMeasurements"
        )
        repeated_measurement: List[ops.Operation] = circuit.filter_by_tag(
            "PragmaRepeatedMeasurement"
        )
        measure_mode: List[ops.Operation] = circuit.filter_by_tag("PhotonDetection")
        if repeated_measurement and measure_mode:
            raise ValueError("Circuit contains multiple ways to set the number of measurements")
        if repeated_measurement and set_measurement:
            raise ValueError("Circuit contains multiple ways to set the number of measurements")

        if set_measurement:
            readout = set_measurement[0].readout()
            shots = set_measurement[0].number_measurements()
        elif repeated_measurement:
            readout = repeated_measurement[0].readout()
            shots = repeated_measurement[0].number_measurements()
        elif measure_mode:
            readout = measure_mode[0].readout()
            shots = 1
        else:
            readout = "ro"
            shots = 100

        program = call_circuit(circuit, self.number_modes)

        if self.__use_actual_hardware:
            if shots > self.__max_number_shots:
                raise ValueError(
                    "Number of shots specified exceeds the number of shots allowed for hardware"
                )
            if len(circuit) > self.__max_circuit_length:
                raise ValueError(
                    "Circuit generated is longer that the max circuit length allowed for hardware"
                )
        return (
            self.__create_device(shots).run(program, shots=shots),
            {"readout_name": readout},
        )

    def run_circuit(
        self, circuit: Circuit
    ) -> Tuple[
        Dict[str, List[List[bool]]],
        Dict[str, List[List[float]]],
        Dict[str, List[List[complex]]],
    ]:
        """Simulate a Circuit on a strawberryfields backend.

        The default number of shots for the simulation is 100.
        Any kind of Measurement instruction only works as intended if
        it is the last instruction in the Circuit.
        Currently only one simulation is performed, meaning different measurements on different
        registers are not supported.

        Args:
            circuit (Circuit): the Circuit to simulate.

        Returns:
            Tuple[Dict[str, List[List[bool]]],
                  Dict[str, List[List[float]]],
                  Dict[str, List[List[complex]]]]: bit, float and complex registers dictionaries.
        """
        (results, metadata) = self._run_circuit(circuit)
        return _post_process_circuit_result(results, metadata)

    def run_measurement_registers(
        self, measurement: Any
    ) -> Tuple[
        Dict[str, List[List[bool]]],
        Dict[str, List[List[float]]],
        Dict[str, List[List[complex]]],
    ]:
        """Run all circuits of a measurement with the StrawberryFields backend.

        Args:
            measurement: The measurement that is run.

        Returns:
            Tuple[Dict[str, List[List[bool]]],
                  Dict[str, List[List[float]]],
                  Dict[str, List[List[complex]]]]
        """
        constant_circuit = measurement.constant_circuit()
        output_bit_register_dict: Dict[str, List[List[bool]]] = {}
        output_float_register_dict: Dict[str, List[List[float]]] = {}
        output_complex_register_dict: Dict[str, List[List[complex]]] = {}

        for circuit in measurement.circuits():
            if constant_circuit is None:
                run_circuit = circuit
            else:
                run_circuit = constant_circuit + circuit

            (
                tmp_bit_register_dict,
                tmp_float_register_dict,
                tmp_complex_register_dict,
            ) = self.run_circuit(run_circuit)

            output_bit_register_dict.update(tmp_bit_register_dict)
            output_float_register_dict.update(tmp_float_register_dict)
            output_complex_register_dict.update(tmp_complex_register_dict)

        return (
            output_bit_register_dict,
            output_float_register_dict,
            output_complex_register_dict,
        )

    def run_measurement(self, measurement: Any) -> Optional[Dict[str, float]]:
        """Run a circuit with the StrawberryFields backend.

        Args:
            measurement: The measurement that is run.

        Returns:
            Optional[Dict[str, float]]
        """
        (
            output_bit_register_dict,
            output_float_register_dict,
            output_complex_register_dict,
        ) = self.run_measurement_registers(measurement)

        return measurement.evaluate(
            output_bit_register_dict,
            output_float_register_dict,
            output_complex_register_dict,
        )
