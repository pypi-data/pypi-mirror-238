# Copyright 2023 Q-CTRL. All rights reserved.
#
# Licensed under the Q-CTRL Terms of service (the "License"). Unauthorized
# copying or use of this file, via any medium, is strictly prohibited.
# Proprietary and confidential. You may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#    https://q-ctrl.com/terms
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS. See the
# License for the specific language.

from functools import wraps
from typing import (
    List,
    Optional,
    Sequence,
    Union,
)

import forge
import numpy as np
from qctrlcommons.node.base import Node
from qctrlcommons.preconditions import (
    check_argument,
    check_argument_iterable,
    check_numeric_numpy_array,
)

from .documentation import Category
from .namespace import create_namespace_doc
from .node_data import (
    Pwc,
    Tensor,
)
from .types import TensorLike
from .utils import (
    check_sample_times_with_bounds,
    validate_ms_shapes,
    validate_shape,
)


def _validate_drives(drives, min_drive_count):
    check_argument_iterable(drives, "drives")
    nonzero_drives = [drive for drive in drives if drive is not None]
    check_argument(
        len(nonzero_drives) >= min_drive_count,
        f"At least {min_drive_count} Pwc drive(s) must be provided.",
        {"drives": drives},
    )
    check_argument(
        all(isinstance(drive, Pwc) for drive in nonzero_drives),
        "Each of the drives must be a Pwc or None.",
        {"drives": drives},
    )
    check_argument(
        all(len(drive.values.shape) == 1 for drive in nonzero_drives),
        "Each of the drives must be scalar valued or None.",
        {"drives": drives},
    )
    duration = sum(nonzero_drives[0].durations)
    check_argument(
        all(np.isclose(sum(drive.durations), duration) for drive in nonzero_drives),
        "All of the Pwc drives must have the same duration.",
        {"drives": drives},
    )

    return nonzero_drives


class MsPhases(Node):
    r"""
    Calculate the relative phases for all pairs of ions described by a Mølmer–Sørensen-type
    interaction when single-tone individually-addressed laser beams are used.

    Use this function to calculate the acquired phases for all ion pairs
    at the final time of the drives, or at the sample times that you provide.

    Parameters
    ----------
    drives : list[Pwc or None]
        The piecewise-constant drives, :math:`\{\gamma_j\}`, one for each of the :math:`N` ions.
        Drive values must be in rad/s and durations must be in seconds.
        All drives must have the same total duration, but can have different segmentations.
        This list must contain at least two elements (your system must contain at least two ions).
        If an ion is not addressed, you can pass None for its drive (this leads to a
        more efficient calculation than passing a zero drive).
    lamb_dicke_parameters : np.ndarray
        The laser-ion coupling strength, :math:`\{\eta_{jkl}\}`.
        Its shape must be ``(3, N, N)``, where the dimensions indicate,
        respectively, axis, collective mode, and ion.
    relative_detunings : np.ndarray
        The difference :math:`\{\delta_{jk} = \nu_{jk} - \delta\}` (in Hz) between each motional
        mode frequency and the laser detuning from the qubit transition frequency :math:`\omega_0`.
        Its shape must be ``(3, N)``, where the dimensions indicate, respectively,
        axis and collective mode.
    sample_times : list or tuple or np.ndarray or None, optional
        The times (in seconds) at which to calculate the relative phases, :math:`\{t_i\}`.
        If you provide it, it must be 1D, ordered, and contain at least one element.
        If you omit it, this function calculates the phases only at the final time of the drives.
    name : str or None, optional
        The name of the node.

    Returns
    -------
    Tensor(real)
        Acquired phases :math:`\{\phi_{jk}(t_i) + \phi_{kj}(t_i)\}` for all ion pairs.
        If you provide `sample_times`, the shape of the returned value is ``(T, N, N)``,
        where the first dimension indicates time, and the second and third dimensions
        indicate ions. Otherwise, the shape is ``(N, N)``, with the outer time dimension removed.
        The relative phases are stored as a strictly lower triangular matrix.
        See the notes part for details.

    See Also
    --------
    :func:`Graph.ions.ms_infidelity <ions.ms_infidelity>`
        Final operational infidelity of a Mølmer–Sørensen gate.
    :func:`Graph.ions.ms_phases_multitone <ions.ms_phases_multitone>`
        Corresponding operation for a global multitone beam.
    :func:`boulderopal.ions.obtain_ion_chain_properties`
        Function to calculate the properties of an ion chain.

    Notes
    -----
    The internal and motional Hamiltonian of :math:`N` ions is

    .. math::
        H_0 = \sum_{j=1}^{3} \sum_{k=1}^{N} \hbar\nu_{jk} \left(a_{jk}^\dagger a_{jk}
            + \frac{1}{2}\right) + \sum_{l=1}^N \frac{\hbar \omega_0}{2} \sigma_{z,l} ,

    where :math:`j` indicates axis dimension (:math:`x`, :math:`y`, or :math:`z`),
    :math:`k` indicates collective mode, :math:`a_{jk}` is the annihilation operator,
    and :math:`\sigma_{z,l}` is the Pauli :math:`Z` operator for ion :math:`l`.

    The interaction Hamiltonian for Mølmer–Sørensen-type
    operations in the rotating frame with respect to :math:`H_0` is

    .. math::
        H_I(t) = i\hbar \sum_{j=1}^{3} \sum_{k=1}^{N} \sum_{l=1}^N
            \sigma_{x,l} \left(-\beta_{jkl}^*(t)a_{jk} + \beta_{jkl}(t) a_{jk}^\dagger\right) ,

    where :math:`\sigma_{x,l}` is the Pauli :math:`X` operator for ion :math:`l` and

    .. math::
        \beta_{jkl}(t) = \eta_{jkl} \frac{\gamma_l(t)}{2} \exp(i 2 \pi \delta_{jk} t)

    indicates the coupling between ion :math:`l` and motional mode :math:`(j,k)`.

    The corresponding unitary operation is given by [1]_

    .. math::
        U(t) = \exp\left[ \sum_{l=1}^N \sigma_{x,l} B_l(t)
            + i\sum_{l=1}^N\sum_{n=1}^{l-1} (\phi_{ln}(t) + \phi_{nl}(t))
            \sigma_{x,l} \sigma_{x,n} \right] ,

    where

    .. math::
        B_l(t) &\equiv \sum_{j=1}^{3} \sum_{k=1}^{N}
            \left(\eta_{jkl}\alpha_{jkl}(t)a_{jk}^\dagger
            - \eta_{jkl}^{\ast}\alpha_{jkl}^\ast(t)a_{jk} \right) ,

        \phi_{ln}(t) &\equiv \mathrm{Im} \left[ \sum_{j=1}^{3} \sum_{k=1}^{N}
            \int_{0}^{t} d \tau_1 \int_{0}^{\tau_1} d \tau_2
            \beta_{jkl}(\tau_1)\beta_{jkn}^{\ast}(\tau_2) \right] ,

        \alpha_{jkl}(t) &\equiv \int_0^t d\tau \frac{\gamma_l(\tau)}{2}
            \exp(i 2 \pi \delta_{jk} \tau) .

    This function calculates the relative phases for all ions pairs
    at sample times :math:`\{t_i\}`,

    .. math::
        \Phi_{ln}(t_i) = \phi_{ln}(t_i) + \phi_{nl}(t_i),

    and stores them in a strictly lower triangular matrix.
    That is, :math:`\Phi_{ln}(t_i)` with :math:`l > n`
    gives the relative phase between ions :math:`l` and :math:`n`,
    while :math:`\Phi_{ln}(t_i) = 0` for :math:`l \leq n`.

    References
    ----------
    .. [1] `C. D. B. Bentley, H. Ball, M. J. Biercuk, A. R. R. Carvalho,
            M. R. Hush, and H. J. Slatyer,
            Adv. Quantum Technol. 3, 2000044 (2020).
            <https://doi.org/10.1002/qute.202000044>`_

    Examples
    --------
    Refer to the `How to optimize error-robust Mølmer–Sørensen gates for trapped ions
    <https://docs.q-ctrl.com/boulder-opal/user-guides/how-to-optimize-error-robust-molmer-
    sorensen-gates-for-trapped-ions>`_ user guide to find how to use this and related nodes.
    """

    name = "ms_phases"
    args = [
        forge.arg("drives", type=Sequence[Optional[Pwc]]),
        forge.arg("lamb_dicke_parameters", type=np.ndarray),
        forge.arg("relative_detunings", type=np.ndarray),
        forge.arg(
            "sample_times", type=Optional[Union[list, tuple, np.ndarray]], default=None
        ),
    ]
    rtype = Tensor
    categories = [Category.MOLMER_SORENSEN]

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        drives = kwargs.get("drives")
        sample_times = kwargs.get("sample_times")
        lamb_dicke_parameters = kwargs.get("lamb_dicke_parameters")
        relative_detunings = kwargs.get("relative_detunings")

        nonzero_drives = _validate_drives(drives, 2)

        ion_count = len(drives)
        shape = (ion_count, ion_count)
        validate_ms_shapes(
            ion_count=ion_count,
            ld_values=lamb_dicke_parameters,
            ld_name="lamb_dicke_parameters",
            rd_values=relative_detunings,
            rd_name="relative_detunings",
        )
        if sample_times is not None:
            sample_times = np.asarray(sample_times)
            check_sample_times_with_bounds(
                sample_times, "sample_times", nonzero_drives[0], "the drives"
            )
            time_count = len(sample_times)
            shape = (time_count,) + tuple(shape)
        return Tensor(_operation, shape=shape)


class MsPhasesMultitone(Node):
    r"""
    Calculate the relative phases for all pairs of ions described by a
    Mølmer–Sørensen-type interaction where the ions are being addressed by
    a multitone global beam.

    Use this function to calculate the acquired phases for all ion pairs
    at the final time of the drives, or at the sample times that you provide.

    Parameters
    ----------
    drives : list[Pwc]
        The piecewise-constant drives, :math:`\{\gamma_j\}`,
        one for each of the :math:`M` tones of the global beam.
        Drive values must be in rad/s and durations must be in seconds.
        All drives must have the same total duration, but can have different segmentations.
    lamb_dicke_parameters : np.ndarray
        The laser-ion coupling strength, :math:`\{\eta_{\xi jkl}\}`.
        Its shape must be ``(M, 3, N, N)``, where the dimensions indicate,
        respectively, tone of the global beam, axis, collective mode, and ion.
    relative_detunings : np.ndarray
        The difference :math:`\{\delta_{\xi jk} = \nu_{jk} - \delta_\xi \}` (in Hz) between
        each motional mode frequency and the laser detunings for each tone from the qubit
        transition frequency :math:`\omega_0`. Its shape must be ``(M, 3, N)``, where the
        dimensions indicate, respectively, tone of the global beam, axis, and collective mode.
    sample_times : list or tuple or np.ndarray or None, optional
        The times (in seconds) at which to calculate the relative phases, :math:`\{t_i\}`.
        If you provide it, it must be 1D, ordered, and contain at least one element.
        If you omit it, this function calculates the phases only at the final time of the drives.
    name : str or None, optional
        The name of the node.

    Returns
    -------
    Tensor(real)
        Acquired phases :math:`\{\phi_{jk}(t_i) + \phi_{kj}(t_i)\}` for all ion pairs.
        If you provide `sample_times`, the shape of the returned value is ``(T, N, N)``,
        where the first dimension indicates time, and the second and third dimensions
        indicate ions. Otherwise, the shape is ``(N, N)``, with the outer time dimension removed.
        The relative phases are stored as a strictly lower triangular matrix.
        See the notes part for details.

    See Also
    --------
    :func:`Graph.ions.ms_infidelity <ions.ms_infidelity>`
        Final operational infidelity of a Mølmer–Sørensen gate.
    :func:`Graph.ions.ms_phases <ions.ms_phases>`
        Corresponding operation for single-tone individually-addressed beams.
    :func:`boulderopal.ions.obtain_ion_chain_properties`
        Function to calculate the properties of an ion chain.

    Notes
    -----
    The interaction Hamiltonian for Mølmer–Sørensen-type
    operations in the rotating frame for a multitone global beam is

    .. math::
        H_I(t) = i\hbar \sum_{\xi=1}^M \sum_{j=1}^{3} \sum_{k=1}^{N} \sum_{l=1}^N \sigma_{x,l}
            \left(-\beta_{\xi jkl}^*(t)a_{jk} + \beta_{\xi jkl}(t) a_{jk}^\dagger\right) ,

    where :math:`\sigma_{x,l}` is the Pauli :math:`X` operator for the ion :math:`l` and

    .. math::

        \beta_{\xi jkl}(t) = \eta_{\xi jkl} \frac{\gamma_\xi(t)}{2} \exp(i 2 \pi \delta_{\xi jk} t)

    indicates the coupling between ion :math:`l` and motional mode :math:`(\xi,j,k)`.

    The corresponding unitary operation is given by

    .. math::
        U(t) = \exp\left[ \sum_{l=1}^N \sigma_{x,l} B_l(t)
                + i\sum_{l=1}^N \sum_{n=1}^{l-1} (\phi_{ln}(t) + \phi_{nl}(t))
                \sigma_{x,l} \sigma_{x,n} \right] ,

    where

    .. math::
        B_l(t) &\equiv \sum_{\xi=1}^M \sum_{j=1}^{3} \sum_{k=1}^{N}
             \left(\eta_{\xi jkl}\alpha_{\xi jkl}(t)a_{jk}^\dagger
             - \eta_{\xi jkl}^{\ast}\alpha_{\xi jkl}^\ast(t)a_{jk} \right) ,

        \phi_{ln}(t) &\equiv \mathrm{Im} \left[
            \sum_{\xi=1}^M \sum_{\chi=1}^M \sum_{j=1}^{3} \sum_{k=1}^{N}
            \int_{0}^{t} d \tau_1 \int_{0}^{\tau_1} d \tau_2
            \beta_{\xi jkl}(\tau_1)\beta_{\chi jkn}^{\ast}(\tau_2) \right] ,

        \alpha_{\xi jkl}(t) &\equiv \int_0^t d\tau \frac{\gamma_\xi(\tau)}{2}
            \exp(i 2 \pi \delta_{\xi jk} \tau).

    This function calculates the relative phases for all ions pairs
    at sample times :math:`\{t_i\}`,

    .. math::
        \Phi_{ln}(t_i) = \phi_{ln}(t_i) + \phi_{nl}(t_i),

    and stores them in a strictly lower triangular matrix.
    That is, :math:`\Phi_{ln}(t_i)` with :math:`l > n`
    gives the relative phase between ions :math:`l` and :math:`n`,
    while :math:`\Phi_{ln}(t_i) = 0` for :math:`l \leq n`.
    """

    name = "ms_phases_multitone"
    args = [
        forge.arg("drives", type=List[Pwc]),
        forge.arg("lamb_dicke_parameters", type=np.ndarray),
        forge.arg("relative_detunings", type=np.ndarray),
        forge.arg(
            "sample_times", type=Optional[Union[list, tuple, np.ndarray]], default=None
        ),
    ]
    rtype = Tensor
    categories = [Category.MOLMER_SORENSEN]

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        drives = kwargs.get("drives")
        sample_times = kwargs.get("sample_times")
        lamb_dicke_parameters = kwargs.get("lamb_dicke_parameters")
        relative_detunings = kwargs.get("relative_detunings")
        check_argument_iterable(drives, "drives")
        check_argument(
            len(drives) > 0, "At least one drive must be provided.", {"drives": drives}
        )
        check_argument(
            all(isinstance(drive, Pwc) for drive in drives),
            "Each of the drives must be a Pwc.",
            {"drives": drives},
        )
        check_argument(
            all(len(drive.values.shape) == 1 for drive in drives),
            "The value of each drive must be 1D.",
            {"drives": drives},
        )

        check_numeric_numpy_array(lamb_dicke_parameters, "lamb_dicke_parameters")
        check_numeric_numpy_array(relative_detunings, "relative_detunings")

        ld_shape = validate_shape(lamb_dicke_parameters, "lamb_dicke_parameters")
        rd_shape = validate_shape(relative_detunings, "relative_detunings")

        tone_count = len(drives)
        ion_count = ld_shape[-1]
        check_argument(
            ld_shape == (tone_count, 3, ion_count, ion_count),
            "The Lamb-Dicke parameters must have shape (tone_count, 3, ion_count, ion_count).",
            {"lamb_dicke_parameters": lamb_dicke_parameters},
            extras={
                "ion_count": ion_count,
                "tone_count": tone_count,
                "lamb_dicke_parameters.shape": ld_shape,
            },
        )
        check_argument(
            rd_shape == (tone_count, 3, ion_count),
            "The relative detunings must have shape (tone_count, 3, ion_count).",
            {"relative_detunings": relative_detunings},
            extras={
                "ion_count": ion_count,
                "tone_count": tone_count,
                "relative_detunings.shape": rd_shape,
            },
        )

        shape = (ion_count, ion_count)
        if sample_times is not None:
            sample_times = np.asarray(sample_times)
            check_sample_times_with_bounds(
                sample_times, "sample_times", drives[0], "drives[0]"
            )
            time_count = len(sample_times)
            shape = (time_count,) + shape

        return Tensor(_operation, shape=shape)


class MsDisplacements(Node):
    r"""
    Calculate the displacements for each mode and ion combination where ions are described by
    a Mølmer–Sørensen-type interaction.

    Use this function to calculate the displacements for each ion and each mode
    at the final time of the drives, or at the sample times that you provide.

    Parameters
    ----------
    drives : list[Pwc or None]
        The piecewise-constant drives, :math:`\{\gamma_j\}`, one for each of the :math:`N` ions.
        Drive values must be in rad/s and durations must be in seconds.
        All drives must have the same total duration, but can have different segmentations.
        If an ion is not addressed, you can pass None for its drive (this leads to a
        more efficient calculation than passing a zero drive).
    lamb_dicke_parameters : np.ndarray
        The laser-ion coupling strength, :math:`\{\eta_{jkl}\}`.
        Its shape must be ``(3, N, N)``, where the dimensions indicate,
        respectively, axis, collective mode, and ion.
    relative_detunings : np.ndarray
        The difference :math:`\{\delta_{jk} = \nu_{jk} - \delta\}` (in Hz) between each motional
        mode frequency and the laser detuning from the qubit transition frequency :math:`\omega_0`.
        Its shape must be ``(3, N)``, where the dimensions indicate, respectively,
        axis and collective mode.
    sample_times : list or tuple or np.ndarray or None, optional
        The times (in seconds) at which to calculate the displacements, :math:`\{t_i\}`.
        If you provide it, it must be 1D, ordered, and contain at least one element.
        If you omit it, this function calculates the phases only at the final time of the drives.
    name : str or None, optional
        The name of the node.

    Returns
    -------
    Tensor(complex)
        Displacements :math:`\{\eta_{jkl}\alpha_{jkl}(t_i)\}` for all mode-ion combinations.
        If you provide `sample_times`, the shape of the returned value is ``(T, 3, N, N_d)``,
        where the dimensions indicate, respectively, time, axis, collective mode, and ion.
        Otherwise, the shape is ``(3, N, N_d)``, with the outer time dimension removed.
        Here, ``N_d`` is the number of addressed ions (drives that are not None);
        the displacements of undriven ions are not returned (as they are zero).

    See Also
    --------
    :func:`Graph.ions.ms_infidelity <ions.ms_infidelity>`
        Final operational infidelity of a Mølmer–Sørensen gate.
    :func:`boulderopal.ions.obtain_ion_chain_properties`
        Function to calculate the properties of an ion chain.

    Notes
    -----
    This function calculates, at sample times :math:`\{t_i\}`, the contribution
    to the displacement of mode :math:`k` in dimension :math:`j` from ion :math:`l`,
    namely :math:`\eta_{jkl}\alpha_{jkl}(t_i)`, where

    .. math::
        \alpha_{jkl}(t) \equiv \int_0^t d\tau \frac{\gamma_l(\tau)}{2}
            \exp(i 2 \pi \delta_{jk} \tau) .

    You can calculate the state-dependent displacement by summing over the contributions
    from all ions. That is, using the displacement superoperator :math:`\mathcal{D}_{jk}`,
    the displacement in phase space for mode :math:`(j,k)` is

    .. math::
        \mathcal{D}_{jk} \left(\sum_{l=1}^N \sigma_{x,l}\eta_{jkl}\alpha_{jkl}(t_i) \right) .

    Examples
    --------
    Refer to the `How to optimize error-robust Mølmer–Sørensen gates for trapped ions
    <https://docs.q-ctrl.com/boulder-opal/user-guides/how-to-optimize-error-robust-molmer-sorensen
    -gates-for-trapped-ions>`_ user guide to find how to use this and related nodes.
    """

    name = "ms_displacements"
    args = [
        forge.arg("drives", type=Sequence[Optional[Pwc]]),
        forge.arg("lamb_dicke_parameters", type=np.ndarray),
        forge.arg("relative_detunings", type=np.ndarray),
        forge.arg(
            "sample_times", type=Optional[Union[list, tuple, np.ndarray]], default=None
        ),
    ]
    rtype = Tensor
    categories = [Category.MOLMER_SORENSEN]

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        drives = kwargs.get("drives")
        sample_times = kwargs.get("sample_times")
        lamb_dicke_parameters = kwargs.get("lamb_dicke_parameters")
        relative_detunings = kwargs.get("relative_detunings")

        nonzero_drives = _validate_drives(drives, 1)

        ion_count = len(drives)
        shape = (3, ion_count, len(nonzero_drives))
        validate_ms_shapes(
            ion_count=ion_count,
            ld_values=lamb_dicke_parameters,
            ld_name="lamb_dicke_parameters",
            rd_values=relative_detunings,
            rd_name="relative_detunings",
        )
        if sample_times is not None:
            sample_times = np.asarray(sample_times)
            check_sample_times_with_bounds(
                sample_times, "sample_times", nonzero_drives[0], "the drives"
            )
            time_count = len(sample_times)
            shape = (time_count,) + tuple(shape)
        return Tensor(_operation, shape=shape)


class MsInfidelity(Node):
    r"""
    Calculate the final operational infidelity of the Mølmer–Sørensen gate.

    This function calculates the operational infidelity with respect to the target phases
    that you specify in the `target_phases` array. It can use the tensors returned from
    :func:`ms_phases` and :func:`ms_displacements` to calculate the infidelity tensor.

    Parameters
    ----------
    phases : np.ndarray(real) or Tensor(real)
        The acquired phases between ion pairs, :math:`\{\Phi_{ln}\}`.
        Its shape must be ``(N, N)`` without time samples or ``(T, N, N)`` with them,
        where ``T`` is the number of samples and ``N`` is the number of ions.
        For each sample, the `phases` array must be a strictly lower triangular matrix.
    displacements : np.ndarray(complex) or Tensor(complex)
        The motional displacements in phase-space, :math:`\{\eta_{jkl} \alpha_{jkl}\}`.
        Its shape must be ``(3, N, N_d)`` without time samples or ``(T, 3, N, N_d)`` with them,
        where the dimensions indicate, respectively, (time,) axis, collective mode, and ion.
        Here, ``N_d`` is the number of addressed ions.
    target_phases : np.ndarray
        The target total relative phases between ion pairs, :math:`\{\Psi_{ln}\}`,
        as a strictly lower triangular matrix of shape ``(N, N)``.
    mean_phonon_numbers : np.ndarray or None, optional
        The mean phonon occupation of motional modes, :math:`\{\bar{n}_{jk}\}`.
        Its shape must be ``(3, N)``, where the dimensions indicate, respectively,
        axis and collective mode.
        If provided, must contain positive real numbers.
        If not provided, :math:`\bar{n}_{jk} = 0`, meaning no occupation of each mode.
    name : str or None, optional
        The name of the node.

    Returns
    -------
    Tensor(real)
        A scalar or 1D tensor of infidelities with shape ``(T,)``.

    See Also
    --------
    :func:`Graph.ions.ms_dephasing_robust_cost <ions.ms_dephasing_robust_cost>`
        Cost for robust optimization of a Mølmer–Sørensen gate.
    :func:`Graph.ions.ms_displacements <ions.ms_displacements>`
        Displacements for each mode/ion combination.
    :func:`Graph.ions.ms_phases <ions.ms_phases>`
        Relative phases for all pairs of ions.

    Notes
    -----
    The infidelity is calculated according to [1]_

    .. math::
        1 - \mathcal{F}_\mathrm{av} = 1 - \left| \left( \prod_{n=1}^N \prod_{l=n+1}^N
            \cos ( \Phi_{ln} - \Psi_{ln}) \right)
            \left( 1 - \sum_{j=1}^3 \sum_{k=1}^N \sum_{l=1}^N \left[ |\eta_{jkl} \alpha_{jkl}|^2
            \left(\bar{n}_{jk}+\frac{1}{2} \right) \right] \right) \right|^2 ,

    which assumes that the displacements :math:`\alpha_{jkl}` are
    small and eliminates terms of the fourth or higher order in them.

    See the notes of :func:`Graph.ions.ms_phases <ions.ms_phases>` or
    :func:`Graph.ions.ms_phases_multitone <ions.ms_phases_multitone>` for the
    relevant definitions.

    References
    ----------
    .. [1] `C. D. B. Bentley, H. Ball, M. J. Biercuk, A. R. R. Carvalho,
            M. R. Hush, and H. J. Slatyer,
            Adv. Quantum Technol. 3, 2000044 (2020).
            <https://doi.org/10.1002/qute.202000044>`_

    Examples
    --------
    Refer to the `How to optimize error-robust Mølmer–Sørensen gates for trapped ions
    <https://docs.q-ctrl.com/boulder-opal/user-guides/how-to-optimize-error-robust-molmer-
    sorensen-gates-for-trapped-ions>`_ user guide to find how to use this and related nodes.
    """

    name = "ms_infidelity"
    args = [
        forge.arg("phases", type=TensorLike),
        forge.arg("displacements", type=TensorLike),
        forge.arg("target_phases", type=np.ndarray),
        forge.arg("mean_phonon_numbers", type=Optional[np.ndarray], default=None),
    ]
    rtype = Tensor
    categories = [Category.MOLMER_SORENSEN]

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        phases = kwargs.get("phases")
        displacements = kwargs.get("displacements")
        target_phases = kwargs.get("target_phases")
        mean_phonon_numbers = kwargs.get("mean_phonon_numbers")
        check_numeric_numpy_array(phases, "phases")
        check_numeric_numpy_array(displacements, "displacements")
        check_numeric_numpy_array(target_phases, "target_phases")
        check_numeric_numpy_array(mean_phonon_numbers, "mean_phonon_numbers")
        phases_shape = validate_shape(phases, "phases")
        displacements_shape = validate_shape(displacements, "displacements")
        target_shape = validate_shape(target_phases, "target_phases")
        ion_count = target_shape[-1]
        check_argument(
            phases_shape[-2:] == (ion_count, ion_count),
            "The shape of phases must be (ion_count, ion_count) or"
            " (sample_count, ion_count, ion_count).",
            {"phases": phases},
            extras={"ion_count": ion_count, "phases.shape": phases_shape},
        )
        check_argument(
            len(phases_shape) <= 3,
            "The shape of phases must have at most 3 dimensions.",
            {"phases": phases},
            extras={"phases.shape": phases_shape},
        )
        check_argument(
            displacements_shape[-3:-1] == (3, ion_count),
            "The shape of displacements must be (3, ion_count, driven_ion_count) or"
            " (sample_count, 3, ion_count, driven_ion_count).",
            {"displacements": displacements},
            extras={"ion_count": ion_count, "displacements.shape": displacements_shape},
        )
        check_argument(
            phases_shape[:-2] == displacements_shape[:-3],
            "If the shape of phases is (sample_count, ion_count, ion_count), then"
            " the shape of displacements must be (sample_count, 3, ion_count, ion_count).",
            {"phases": phases, "displacements": displacements},
            extras={
                "phases.shape": phases_shape,
                "displacements.shape": displacements_shape,
            },
        )
        check_argument(
            target_shape == (ion_count, ion_count),
            "The shape of target_phases must be (ion_count, ion_count).",
            {"target_phases": target_phases},
            extras={"ion_count": ion_count, "target_phases.shape": target_shape},
        )
        check_argument(
            np.allclose(target_phases, np.tril(target_phases, k=-1)),
            "The target_phases matrix must be strictly lower-triangular.",
            {"target_phases": target_phases},
        )
        if mean_phonon_numbers is not None:
            phonon_shape = validate_shape(mean_phonon_numbers, "mean_phonon_numbers")
            check_argument(
                phonon_shape == (3, ion_count),
                "The shape of mean_phonon_numbers must be (3, ion_count).",
                {"mean_phonon_numbers": mean_phonon_numbers},
                extras={
                    "ion_count": ion_count,
                    "mean_phonon_number.shape": phonon_shape,
                },
            )
        shape = phases_shape[:-2]
        return Tensor(_operation, shape=shape)


class MsDephasingRobustCost(Node):
    r"""
    Calculate the cost for robust optimization of a Mølmer–Sørensen gate.

    Add the tensor that this function returns to the infidelity of your
    target operation to obtain a cost that you can use to create a
    Mølmer–Sørensen gate that is robust against dephasing noise. You can
    further multiply the robust cost by a scaling factor to weigh how much
    importance you give to the robustness compared to the original cost.

    Parameters
    ----------
    drives : list[Pwc or None]
        The piecewise-constant drives, :math:`\{\gamma_j\}`, one for each of the :math:`N` ions.
        Drive values must be in rad/s and durations must be in seconds.
        All drives must have the same total duration, but can have different segmentations.
        If an ion is not addressed, you can pass None for its drive (this leads to a
        more efficient calculation than passing a zero drive).
    lamb_dicke_parameters : np.ndarray
        The laser-ion coupling strength, :math:`\{\eta_{jkl}\}`.
        Its shape must be ``(3, N, N)``, where the dimensions indicate,
        respectively, axis, collective mode, and ion.
    relative_detunings : np.ndarray
        The difference :math:`\{\delta_{jk} = \nu_{jk} - \delta\}` (in Hz) between each motional
        mode frequency and the laser detuning from the qubit transition frequency :math:`\omega_0`.
        Its shape must be ``(3, N)``, where the dimensions indicate, respectively,
        axis and collective mode.
    name : str or None, optional
        The name of the node.

    Returns
    -------
    Tensor(scalar, real)
        The cost term that you can use to optimize a Mølmer–Sørensen gate
        that is robust against dephasing noise. The cost is the sum of the
        square moduli of the time-averaged positions of the phase-space
        trajectories, weighted by the corresponding Lamb–Dicke parameters.

    See Also
    --------
    :func:`Graph.ions.ms_infidelity <ions.ms_infidelity>`
        Final operational infidelity of a Mølmer–Sørensen gate.
    :func:`boulderopal.ions.obtain_ion_chain_properties`

    Notes
    -----
    You can construct a Mølmer–Sørensen gate that is robust against
    dephasing noise by a combination of minimizing the time-averaged
    positions of the phase-space trajectories and imposing a symmetry in
    each ion's drive [1]_.

    The displacement of the :math:`l`-th ion in the :math:`k`-th mode of
    oscillation in dimension :math:`j` is [2]_

    .. math::
        \alpha_{jkl}(t) = \int_0^t d\tau \frac{\gamma_l(\tau)}{2}
                \exp(i 2 \pi \delta_{jk} \tau) .

    For a gate of duration :math:`t_\text{gate}`, the time-averaged displacement is

    .. math::
        \langle \alpha_{jkl} \rangle = \frac{1}{t_\text{gate}}
                \int_0^{t_\text{gate}} \alpha_{jkl}(t) \mathrm{d} t .

    This function returns the sum of the square moduli of the time-averaged
    positions multiplied by the corresponding Lamb–Dicke parameters. These
    parameters weight the time-averaged positions in the same way that the
    :math:`\alpha_{jkl}(t)` are weighted in the formula for the infidelity
    of a Mølmer–Sørensen gate (see :func:`Graph.ions.ms_infidelity <ions.ms_infidelity>`).

    In other words, the robust cost that this function returns is

    .. math::
        C_\text{robust} = \sum_{j=1}^{3} \sum_{k=1}^{N} \sum_{l=1}^{N}
            \left| \eta_{jkl} \langle \alpha_{jkl} \rangle \right|^2 .

    You can add this to the infidelity with the respect to the target gate
    to create the cost function that optimizes a gate that is also robust
    against dephasing. You can further multiply :math:`C_\text{robust}` by
    a scaling factor to weigh how much importance you give to robustness.

    References
    ----------
    .. [1] `A. R. Milne, C. L. Edmunds, C. Hempel, F. Roy, S. Mavadia,
            and M. J. Biercuk,
            Phys. Rev. Appl. 13, 024022 (2020).
            <https://doi.org/10.1103/PhysRevApplied.13.024022>`_
    .. [2] `C. D. B. Bentley, H. Ball, M. J. Biercuk, A. R. R. Carvalho,
            M. R. Hush, and H. J. Slatyer,
            Adv. Quantum Technol. 3, 2000044 (2020).
            <https://doi.org/10.1002/qute.202000044>`_

    Examples
    --------
    Refer to the `How to optimize error-robust Mølmer–Sørensen gates for trapped ions
    <https://docs.q-ctrl.com/boulder-opal/user-guides/how-to-optimize-error-robust-molmer-
    sorensen-gates-for-trapped-ions>`_ user guide to find how to use this and related nodes.
    """

    name = "ms_dephasing_robust_cost"
    args = [
        forge.arg("drives", type=Sequence[Optional[Pwc]]),
        forge.arg("lamb_dicke_parameters", type=np.ndarray),
        forge.arg("relative_detunings", type=np.ndarray),
    ]
    rtype = Tensor
    categories = [Category.MOLMER_SORENSEN]

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        drives = kwargs.get("drives")
        lamb_dicke_parameters = kwargs.get("lamb_dicke_parameters")
        relative_detunings = kwargs.get("relative_detunings")

        _validate_drives(drives, 1)

        ion_count = len(drives)
        validate_ms_shapes(
            ion_count=ion_count,
            ld_values=lamb_dicke_parameters,
            ld_name="lamb_dicke_parameters",
            rd_values=relative_detunings,
            rd_name="relative_detunings",
        )
        return Tensor(_operation, shape=())


class IonsNamespace:
    """
    Operations to describeMølmer–Sørensen interactions.
    """

    __name__ = "ions"

    def __init__(self, graph):
        self._graph = graph

    # pylint: disable=missing-function-docstring
    @wraps(MsDephasingRobustCost.create_graph_method())
    def ms_dephasing_robust_cost(self, *args, **kwargs):
        return MsDephasingRobustCost.create_graph_method()(self._graph, *args, **kwargs)

    @wraps(MsDisplacements.create_graph_method())
    def ms_displacements(self, *args, **kwargs):
        return MsDisplacements.create_graph_method()(self._graph, *args, **kwargs)

    @wraps(MsInfidelity.create_graph_method())
    def ms_infidelity(self, *args, **kwargs):
        return MsInfidelity.create_graph_method()(self._graph, *args, **kwargs)

    @wraps(MsPhases.create_graph_method())
    def ms_phases(self, *args, **kwargs):
        return MsPhases.create_graph_method()(self._graph, *args, **kwargs)

    @wraps(MsPhasesMultitone.create_graph_method())
    def ms_phases_multitone(self, **kwargs):
        return MsPhasesMultitone.create_graph_method()(self._graph, **kwargs)


IonsNamespaceDoc = create_namespace_doc("ions", __name__, [Category.MOLMER_SORENSEN])
