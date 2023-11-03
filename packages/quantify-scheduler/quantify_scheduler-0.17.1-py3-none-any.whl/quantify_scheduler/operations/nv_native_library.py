# Repository: https://gitlab.com/quantify-os/quantify-scheduler
# Licensed according to the LICENCE file on the main branch
# pylint: disable=invalid-name
"""NV-center-specific operations for use with the quantify_scheduler."""
from typing import Literal, Tuple, Union
from .operation import Operation
from ..enums import BinMode


class ChargeReset(Operation):
    r"""
    Prepare a NV to its negative charge state NV$^-$.
    """

    def __init__(self, *qubits: str):
        """
        Create a new instance of ChargeReset operation that is used to initialize the
        charge state of an NV center.

        Parameters
        ----------
        qubit
            The qubit to charge-reset. NB one or more qubits can be specified, e.g.,
            :code:`ChargeReset("qe0")`, :code:`ChargeReset("qe0", "qe1", "qe2")`, etc..
        """

        super().__init__(name=f"ChargeReset {', '.join(qubits)}")
        self.data.update(
            {
                "name": f"ChargeReset {', '.join(qubits)}",
                "gate_info": {
                    "unitary": None,
                    "plot_func": "quantify_scheduler.schedules._visualization."
                    + "circuit_diagram.reset",
                    "tex": r"$NV^-$",
                    "qubits": list(qubits),
                    "operation_type": "charge_reset",
                },
            }
        )
        self.update()

    def __str__(self) -> str:
        qubits = map(lambda x: f"'{x}'", self.data["gate_info"]["qubits"])
        return f'{self.__class__.__name__}({",".join(qubits)})'


class CRCount(Operation):
    r"""
    run the ionization laser and the spin pump laser with a photon count to perform a
    charge and resonance count.
    """

    def __init__(
        self,
        *qubits: str,
        acq_index: Union[Tuple[int, ...], int] = None,
        # These are the currently supported acquisition protocols.
        acq_protocol: Literal[
            "Trace",
            "TriggerCount",
            None,
        ] = None,
        bin_mode: BinMode = None,
    ):
        """
        Gate level description for an optical CR count measurement.

        The measurement is compiled according to the type of acquisition specified
        in the device configuration.

        Parameters
        ----------
        qubits
            The qubits you want to measure
        acq_index
            Index of the register where the measurement is stored.
            If None specified, it will default to a list of zeros of len(qubits)
        acq_protocol
            Acquisition protocol (currently ``"TriggerCount"`` and ``"Trace"``)
            are supported. If ``None`` is specified, the default protocol is chosen
            based on the device and backend configuration.
        bin_mode
            The binning mode that is to be used. If not None, it will overwrite
            the binning mode used for Measurements in the quantum-circuit to
            quantum-device compilation step.
        """

        # this if else statement a workaround to support multiplexed measurements (#262)

        # this snippet has some automatic behaviour that is error prone.
        # see #262
        if len(qubits) == 1:
            if acq_index is None:
                acq_index = 0
        else:
            if isinstance(acq_index, int):
                acq_index = [
                    acq_index,
                ] * len(qubits)
            elif acq_index is None:
                # defaults to writing the result of all qubits to acq_index 0.
                # note that this will result in averaging data together if multiple
                # measurements are present in the same schedule (#262)
                acq_index = list(0 for i in range(len(qubits)))

        plot_func = (
            "quantify_scheduler.schedules._visualization.circuit_diagram.acq_meter_text"
        )
        super().__init__(f"CRCount {', '.join(qubits)}")
        self.data.update(
            {
                "name": f"CRCount {', '.join(qubits)}",
                "gate_info": {
                    "unitary": None,
                    "plot_func": plot_func,
                    "tex": r"CR",
                    "qubits": list(qubits),
                    "acq_index": acq_index,
                    "acq_protocol": acq_protocol,
                    "bin_mode": bin_mode,
                    "operation_type": "cr_count",
                },
            }
        )
        self._update()

    def __str__(self) -> str:
        gate_info = self.data["gate_info"]
        qubits = map(lambda x: f"'{x}'", gate_info["qubits"])
        acq_index = gate_info["acq_index"]
        acq_protocol = gate_info["acq_protocol"]
        bin_mode = gate_info["bin_mode"]
        return (
            f'{self.__class__.__name__}({",".join(qubits)}, '
            f'acq_index={acq_index}, acq_protocol="{acq_protocol}", '
            f"bin_mode={str(bin_mode)})"
        )
