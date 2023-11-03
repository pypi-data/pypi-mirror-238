# Repository: https://gitlab.com/quantify-os/quantify-scheduler
# Licensed according to the LICENCE file on the main branch

from qcodes.instrument.base import Instrument
from quantify_scheduler.backends.graph_compilation import DeviceCompilationConfig


class DeviceElement(Instrument):
    """
    A device element is responsible for managing parameters of the device
    configuration responsible for compiling operations applied to that specific
    device element from the quantum-circuit to the quantum-device layer.
    """

    def __init__(self, name: str, **kwargs) -> None:
        if "-" in name or "_" in name:
            raise ValueError(
                f"Invalid DeviceElement name '{name}'. Hyphens and "
                f"underscores are not allowed due to naming conventions"
            )
        super().__init__(name, **kwargs)

    def __getstate__(self):
        """
        Serializes `DeviceElement` and derived classes into a dict containing the name
        of the device element and a dict for each submodule containing its
        parameter names and corresponding values.
        """
        snapshot = self.snapshot()

        element_data = {"name": self.name}
        for submodule_name, submodule_data in snapshot["submodules"].items():
            element_data[submodule_name] = {
                name: data["value"]
                for name, data in submodule_data["parameters"].items()
            }

        state = {
            "deserialization_type": self.__class__.__name__,  # Will return derived class name
            "mode": "__init__",
            "data": element_data,
        }
        return state

    def generate_device_config(self) -> DeviceCompilationConfig:
        """
        Generates the device configuration
        """
        raise NotImplementedError
