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

__version__ = "1.1.0"

from qctrlworkflowclient.utils import PackageInfo as _PackageInfo
from qctrlworkflowclient.utils import check_package_version as _check_package_version

from boulderopal import (
    closed_loop,
    cloud,
    gradient_free,
    graph,
    ions,
    noise_reconstruction,
    optimization,
    signals,
    stochastic,
    superconducting,
)
from boulderopal._configuration.configuration import (
    set_cloud_mode,
    set_local_mode,
)
from boulderopal._utils import (
    cite,
    print_package_versions,
)
from boulderopal.gradient_free import run_gradient_free_optimization
from boulderopal.graph import (
    Graph,
    execute_graph,
)
from boulderopal.optimization import run_optimization
from boulderopal.stochastic import run_stochastic_optimization

_check_package_version(
    _PackageInfo(
        name="Boulder Opal client",
        install_name="boulder-opal",
        import_name="boulderopal",
        changelog_url="https://docs.q-ctrl.com/boulder-opal/changelog",
    )
)


__all__ = [
    "Graph",
    "cite",
    "closed_loop",
    "cloud",
    "execute_graph",
    "gradient_free",
    "graph",
    "ions",
    "noise_reconstruction",
    "optimization",
    "print_package_versions",
    "run_gradient_free_optimization",
    "run_optimization",
    "run_stochastic_optimization",
    "set_cloud_mode",
    "set_local_mode",
    "signals",
    "stochastic",
    "superconducting",
]
