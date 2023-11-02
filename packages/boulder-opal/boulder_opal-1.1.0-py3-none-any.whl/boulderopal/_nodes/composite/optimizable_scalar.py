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

from __future__ import annotations

from typing import Optional

import numpy as np

from boulderopal._nodes.documentation import Category
from boulderopal._nodes.node_data import Tensor
from boulderopal._validation.basic import ScalarDType

from .namespace import composite_node


@composite_node([Category.OPTIMIZATION_VARIABLES])
def optimizable_scalar(
    graph: "Graph",
    lower_bound: float,
    upper_bound: float,
    is_lower_unbounded: bool = False,
    is_upper_unbounded: bool = False,
    initial_values: Optional[float | list[float]] = None,
    name: Optional[str] = None,
) -> Tensor:
    r"""
    Create an optimizable scalar Tensor, which can be bounded, semi-bounded, or unbounded.

    Use this function to create a single variable that can be tuned by
    the optimizer to minimize the cost function.

    Parameters
    ----------
    graph : Graph
        The graph object where the node will belong.
    lower_bound : float
        The lower bound :math:`v_\mathrm{min}` for generating an initial value for the variable.
        This will also be used as lower bound if the variable is lower bounded.
    upper_bound : float
        The upper bound :math:`v_\mathrm{max}` for generating an initial value for the variable.
        This will also be used as upper bound if the variable is upper bounded.
    is_lower_unbounded : bool, optional
        Defaults to False. Set this flag to True to define a semi-bounded variable with
        lower bound :math:`-\infty`; in this case, the `lower_bound` parameter is used only for
        generating an initial value.
    is_upper_unbounded : bool, optional
        Defaults to False. Set this flag to True to define a semi-bounded variable with
        upper bound :math:`+\infty`; in this case, the `upper_bound` parameter is used only for
        generating an initial value.
    initial_values : float or List[float] or None, optional
        Initial values for the optimization variable. You can either provide a single initial
        value, or a list of them. Note that all optimization variables in a graph with non-default
        initial values must have the same length. That is, you must set them all either as a single
        value or a list of values of the same length. Defaults to None, meaning the optimizer
        initializes the variable with a random value.
    name : str or None, optional
        The name of the node.

    Returns
    -------
    Tensor
        The :math:`v` optimizable scalar. If both `is_lower_unbounded` and `is_upper_unbounded` are
        False, the variables is bounded such that :math:`v_\mathrm{min}\leq v \leq v_\mathrm{max}`.
        If one of the flags is True (for example `is_lower_unbounded=True`), the variable is
        semi-bounded (for example :math:`-\infty \leq v \leq v_\mathrm{max}`).
        If both of them are True, then the variable is unbounded and satisfies that
        :math:`-\infty \leq v \leq +\infty`.

    See Also
    --------
    Graph.optimization_variable : Create 1D Tensor of optimization variables.
    boulderopal.run_optimization :
        Function to find the minimum of a generic function.
    """

    if initial_values is not None:

        def _validator(name: str):
            return ScalarDType.REAL(name).ge(lower_bound).le(upper_bound)

        if isinstance(initial_values, list):
            initial_values = [
                np.array([_validator(f"initial_values[{idx}]")(value)])
                for idx, value in enumerate(initial_values)
            ]
        else:
            initial_values = np.array([_validator("initial_values")(initial_values)])

    scalar = graph.optimization_variable(
        count=1,
        lower_bound=lower_bound,
        upper_bound=upper_bound,
        is_lower_unbounded=is_lower_unbounded,
        is_upper_unbounded=is_upper_unbounded,
        initial_values=initial_values,
    )[0]

    if name is not None:
        scalar.name = name

    return scalar
