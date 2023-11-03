# Repository: https://gitlab.com/quantify-os/quantify-scheduler
# Licensed according to the LICENCE file on the main branch
"""
A module containing factory functions for pulses on the quantum-device layer.

These factories are used to take a parametrized representation of on a operation
and use that to create an instance of the operation itself.
"""
from __future__ import annotations

import math

import numpy as np

from quantify_scheduler.backends.qblox import constants as qblox_constants
from quantify_scheduler.backends.qblox import helpers as qblox_helpers
from quantify_scheduler.operations import pulse_library
from quantify_scheduler.operations.stitched_pulse import (
    StitchedPulse,
    StitchedPulseBuilder,
)
from quantify_scheduler.resources import BasebandClockResource


def rxy_drag_pulse(
    amp180: float,
    motzoi: float,
    theta: float,
    phi: float,
    port: str,
    duration: float,
    clock: str,
    reference_magnitude: pulse_library.ReferenceMagnitude | None = None,
) -> pulse_library.DRAGPulse:
    """
    Generate a :class:`~.operations.pulse_library.DRAGPulse` that achieves the right
    rotation angle `theta` based on a calibrated pi-pulse amplitude and motzoi
    parameter based on linear interpolation of the pulse amplitudes.

    Parameters
    ----------
    amp180
        Unitless amplitude of excitation pulse to get the maximum 180 degree theta.
    motzoi
        Unitless amplitude of the derivative component, the DRAG-pulse parameter.
    theta
        Angle in degrees to rotate around an equatorial axis on the Bloch sphere.
    phi
        Phase of the pulse in degrees.
    port
        Name of the port where the pulse is played.
    duration
        Duration of the pulse in seconds.
    clock
        Name of the clock used to modulate the pulse.
    reference_magnitude : :class:`~quantify_scheduler.operations.pulse_library.ReferenceMagnitude`, optional
        Optional scaling value and unit for the unitless amplitude. Uses settings in
        hardware config if not provided.

    Returns
    -------
    :
        DRAGPulse operation.
    """
    # G_amp is the gaussian amplitude introduced in
    # https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.103.110501
    # 180 refers to the normalization, theta is in degrees, and
    # amp180 is the amplitude necessary to get the
    # maximum 180 degree theta (experimentally)
    G_amp = amp180 * theta / 180
    D_amp = motzoi

    return pulse_library.DRAGPulse(
        G_amp=G_amp,
        D_amp=D_amp,
        phase=phi,
        port=port,
        duration=duration,
        clock=clock,
        reference_magnitude=reference_magnitude,
    )


def rxy_gauss_pulse(
    amp180: float,
    theta: float,
    phi: float,
    port: str,
    duration: float,
    clock: str,
    reference_magnitude: pulse_library.ReferenceMagnitude | None = None,
) -> pulse_library.GaussPulse:
    """
    Generate a Gaussian drive with :class:`~.operations.pulse_library.GaussPulse` that achieves the right
    rotation angle `theta` based on a calibrated pi-pulse amplitude.

    Parameters
    ----------
    amp180
        Unitless amplitude of excitation pulse to get the maximum 180 degree theta.
    theta
        Angle in degrees to rotate around an equatorial axis on the Bloch sphere.
    phi
        Phase of the pulse in degrees.
    port
        Name of the port where the pulse is played.
    duration
        Duration of the pulse in seconds.
    clock
        Name of the clock used to modulate the pulse.
    reference_magnitude : :class:`~quantify_scheduler.operations.pulse_library.ReferenceMagnitude`, optional
        Optional scaling value and unit for the unitless amplitude. Uses settings in
        hardware config if not provided.

    Returns
    -------
    :
        GaussPulse operation.
    """
    # theta is in degrees, and
    # amp180 is the amplitude necessary to get the
    # maximum 180 degree theta (experimentally)
    G_amp = amp180 * theta / 180

    return pulse_library.GaussPulse(
        G_amp=G_amp,
        phase=phi,
        port=port,
        duration=duration,
        clock=clock,
        reference_magnitude=reference_magnitude,
    )


def phase_shift(
    theta: float,
    clock: str,
) -> pulse_library.ShiftClockPhase:
    """
    Generate a :class:`~.operations.pulse_library.ShiftClockPhase` that shifts the phase of the `clock` by an angle `theta`.

    Parameters
    ----------
    theta
        Angle to shift the clock by, in degrees.
    clock
        Name of the clock to shift.

    Returns
    -------
    :
        ShiftClockPhase operation.
    """
    return pulse_library.ShiftClockPhase(
        phase_shift=theta,
        clock=clock,
    )


def composite_square_pulse(  # pylint: disable=too-many-arguments
    square_amp: float,
    square_duration: float,
    square_port: str,
    square_clock: str,
    virt_z_parent_qubit_phase: float,
    virt_z_parent_qubit_clock: str,
    virt_z_child_qubit_phase: float,
    virt_z_child_qubit_clock: str,
    reference_magnitude: pulse_library.ReferenceMagnitude | None = None,
    t0: float = 0,
) -> pulse_library.SquarePulse:
    """
    This is an example composite pulse to implement a CZ gate. It applies the
    square pulse and then corrects for the phase shifts on both the qubits.

    Parameters
    ----------
    square_amp
        Amplitude of the square envelope.
    square_duration
        The square pulse duration in seconds.
    square_port
        Port of the pulse, must be capable of playing a complex waveform.
    square_clock
        Clock used to modulate the pulse.
    virt_z_parent_qubit_phase
        The phase shift in degrees applied to the parent qubit.
    virt_z_parent_qubit_clock
        The clock of which to shift the phase applied to the parent qubit.
    virt_z_child_qubit_phase
        The phase shift in degrees applied to the child qubit.
    virt_z_child_qubit_clock
        The clock of which to shift the phase applied to the child qubit.
    reference_magnitude : :class:`~quantify_scheduler.operations.pulse_library.ReferenceMagnitude`, optional
        Scaling value and unit for the unitless amplitude. Uses settings in
        hardware config if not provided.
    t0
        Time in seconds when to start the pulses relative to the start time
        of the Operation in the Schedule.

    Returns
    -------
    :
        SquarePulse operation.
    """

    # Start the flux pulse
    composite_pulse = pulse_library.SquarePulse(
        amp=square_amp,
        reference_magnitude=reference_magnitude,
        duration=square_duration,
        port=square_port,
        clock=square_clock,
        t0=t0,
    )

    # And at the same time apply clock phase corrections
    composite_pulse.add_pulse(
        pulse_library.ShiftClockPhase(
            phase_shift=virt_z_parent_qubit_phase,
            clock=virt_z_parent_qubit_clock,
            t0=t0,
        )
    )
    composite_pulse.add_pulse(
        pulse_library.ShiftClockPhase(
            phase_shift=virt_z_child_qubit_phase,
            clock=virt_z_child_qubit_clock,
            t0=t0,
        )
    )

    return composite_pulse


def nv_spec_pulse_mw(
    duration: float,
    amplitude: float,
    clock: str,
    port: str,
    reference_magnitude: pulse_library.ReferenceMagnitude | None = None,
) -> pulse_library.SkewedHermitePulse:
    """Generate hermite pulse for spectroscopy experiment.

    This is a simplified version of the SkewedHermitePulse. It is not skewed. It also
    sets the phase to 0. This means that no rotation about the z-axis is applied on the
    qubit.

    Parameters
    ----------
    duration
        Pulse duration in seconds
    amplitude
        Amplitude of the hermite pulse
    skewness
        Skewness of hermite pulse
    clock
        Name of clock for frequency modulation of hermite pulse
    port
        Name of port where hermite pulse is applied
    reference_magnitude : :class:`~quantify_scheduler.operations.pulse_library.ReferenceMagnitude`, optional
        Scaling value and unit for the unitless amplitude. Uses settings in
        hardware config if not provided.

    Returns
    -------
    :
        Hermite pulse operation
    """
    return pulse_library.SkewedHermitePulse(
        duration=duration,
        amplitude=amplitude,
        reference_magnitude=reference_magnitude,
        skewness=0,
        phase=0,
        clock=clock,
        port=port,
    )


def long_square_pulse(
    amp: float,
    duration: float,
    port: str,
    clock: str = BasebandClockResource.IDENTITY,
    t0: float = 0,
    grid_time_ns: int = qblox_constants.GRID_TIME,
    reference_magnitude: pulse_library.ReferenceMagnitude | None = None,
) -> StitchedPulse:
    """Create a long square pulse using DC voltage offsets.

    .. note::

        This function creates a
        :class:`~quantify_scheduler.operations.stitched_pulse.StitchedPulse` object,
        which can currently only be compiled by the Qblox backend.

    Parameters
    ----------
    amp : float
        Amplitude of the envelope.
    duration : float
        The pulse duration in seconds.
    port : str
        Port of the pulse, must be capable of playing a complex waveform.
    clock : str, optional
        Clock used to modulate the pulse. By default the baseband clock.
    t0 : float, optional
        Time in seconds when to start the pulses relative to the start time
        of the Operation in the Schedule. By default 0.
    grid_time_ns : int, optional
        Grid time in ns. The duration of the long_square_pulse must be a multiple
        of this. By default equal to the grid time of Qblox modules.
    reference_magnitude : :class:`~quantify_scheduler.operations.pulse_library.ReferenceMagnitude`, optional
        Scaling value and unit for the unitless amplitude. Uses settings in
        hardware config if not provided.

    Returns
    -------
    StitchedPulse
        A StitchedPulse object containing an offset instruction with the specified
        amplitude.

    Raises
    ------
    ValueError
        When the duration of the pulse is not a multiple of ``grid_time_ns``.
    """
    try:
        duration = qblox_helpers.to_grid_time(duration, grid_time_ns) * 1e-9
    except ValueError as err:
        raise ValueError(
            f"The duration of a long_square_pulse must be a multiple of "
            f"{grid_time_ns} ns."
        ) from err

    pulse = (
        StitchedPulseBuilder(port=port, clock=clock, t0=t0)
        .add_voltage_offset(
            path_0=amp,
            path_1=0.0,
            duration=duration,
            reference_magnitude=reference_magnitude,
        )
        .build()
    )
    return pulse


def staircase_pulse(
    start_amp: float,
    final_amp: float,
    num_steps: int,
    duration: float,
    port: str,
    clock: str = BasebandClockResource.IDENTITY,
    t0: float = 0,
    grid_time_ns: int = qblox_constants.GRID_TIME,
    reference_magnitude: pulse_library.ReferenceMagnitude | None = None,
) -> StitchedPulse:
    """Create a staircase-shaped pulse using DC voltage offsets.

    This function generates a real valued staircase pulse, which reaches its final
    amplitude in discrete steps. In between it will maintain a plateau.

    .. note::

        This function returns a
        :class:`~quantify_scheduler.operations.stitched_pulse.StitchedPulse` object,
        which can currently only be compiled by the Qblox backend.

    Parameters
    ----------
    start_amp : float
        Starting amplitude of the staircase envelope function.
    final_amp : float
        Final amplitude of the staircase envelope function.
    num_steps : int
        The number of plateaus.
    duration : float
        Duration of the pulse in seconds.
    port : str
        Port of the pulse.
    clock : str, optional
        Clock used to modulate the pulse. By default the baseband clock.
    t0 : float, optional
        Time in seconds when to start the pulses relative to the start time
        of the Operation in the Schedule. By default 0.
    grid_time_ns : int, optional
        Grid time in ns. The duration of each step of the staircase must be a multiple
        of this. By default equal to the grid time of Qblox modules.
    reference_magnitude : :class:`~quantify_scheduler.operations.pulse_library.ReferenceMagnitude`, optional
        Scaling value and unit for the unitless amplitude. Uses settings in
        hardware config if not provided.

    Returns
    -------
    StitchedPulse
        A StitchedPulse object containing incrementing or decrementing offset
        instructions.

    Raises
    ------
    ValueError
        When the duration of a step is not a multiple of ``grid_time_ns``.
    """

    builder = StitchedPulseBuilder(port=port, clock=clock, t0=t0)

    try:
        step_duration = (
            qblox_helpers.to_grid_time(duration / num_steps, grid_time_ns) * 1e-9
        )
    except ValueError as err:
        raise ValueError(
            f"The duration of each step of the staircase must be a multiple of"
            f" {grid_time_ns} ns."
        ) from err
    amps = np.linspace(start_amp, final_amp, num_steps)
    for amp in amps:
        builder.add_voltage_offset(
            path_0=amp,
            path_1=0.0,
            duration=step_duration,
            reference_magnitude=reference_magnitude,
        )
    pulse = builder.build()
    return pulse


def long_ramp_pulse(
    amp: float,
    duration: float,
    port: str,
    offset: float = 0,
    clock: str = BasebandClockResource.IDENTITY,
    t0: float = 0,
    part_duration_ns: int = qblox_constants.STITCHED_PULSE_PART_DURATION_NS,
    reference_magnitude: pulse_library.ReferenceMagnitude | None = None,
) -> StitchedPulse:
    """Creates a long ramp pulse by stitching together shorter ramps.

    This function creates a long ramp pulse by stitching together ramp pulses of the
    specified duration ``part_duration_ns``, with DC voltage offset instructions placed
    in between.

    .. note::

        This function returns a
        :class:`~quantify_scheduler.operations.stitched_pulse.StitchedPulse` object,
        which can currently only be compiled by the Qblox backend.

    Parameters
    ----------
    amp : float
        Amplitude of the ramp envelope function.
    duration : float
        The pulse duration in seconds.
    port : str
        Port of the pulse.
    offset : float, optional
        Starting point of the ramp pulse. By default 0.
    clock : str, optional
        Clock used to modulate the pulse, by default a BasebandClock is used.
    t0 : float, optional
        Time in seconds when to start the pulses relative to the start time of the
        Operation in the Schedule. By default 0.
    part_duration_ns : int, optional
        Duration of each partial ramp in nanoseconds, by default
        :class:`~quantify_scheduler.backends.qblox.constants.STITCHED_PULSE_PART_DURATION_NS`.
    reference_magnitude : :class:`~quantify_scheduler.operations.pulse_library.ReferenceMagnitude`, optional
        Scaling value and unit for the unitless amplitude. Uses settings in
        hardware config if not provided.

    Returns
    -------
    StitchedPulse
        A ``StitchedPulse`` composed of shorter ramp pulses with varying DC offsets,
        forming one long ramp pulse.
    """
    dur_ns = qblox_helpers.to_grid_time(duration)
    num_whole_parts = (dur_ns - 1) // part_duration_ns
    amp_part = part_duration_ns / dur_ns * amp
    dur_left = (dur_ns - num_whole_parts * part_duration_ns) * 1e-9
    amp_left = amp - num_whole_parts * amp_part

    builder = StitchedPulseBuilder(port=port, clock=clock, t0=t0)

    cur_offset = offset
    for _ in range(num_whole_parts):
        if not (math.isclose(offset, 0) and math.isclose(cur_offset, offset)):
            builder.add_voltage_offset(
                path_0=cur_offset, path_1=0.0, reference_magnitude=reference_magnitude
            )
        builder.add_pulse(
            pulse_library.RampPulse(
                amp=amp_part,
                duration=part_duration_ns * 1e-9,
                port=port,
                reference_magnitude=reference_magnitude,
            )
        )
        cur_offset += amp_part
    if cur_offset != offset:
        builder.add_voltage_offset(
            path_0=cur_offset, path_1=0.0, reference_magnitude=reference_magnitude
        )
    builder.add_pulse(
        pulse_library.RampPulse(
            amp=amp_left,
            duration=dur_left,
            port=port,
            reference_magnitude=reference_magnitude,
        )
    )

    pulse = builder.build()

    return pulse
