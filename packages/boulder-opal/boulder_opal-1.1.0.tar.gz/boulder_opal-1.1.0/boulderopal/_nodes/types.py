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
from typing import Union

import numpy as np

from .node_data import (
    Pwc,
    Stf,
    Tensor,
)

TensorLike = Union[np.ndarray, Tensor]
TensorLikeOrFunction = Union[np.ndarray, Tensor, Pwc, Stf]
NumericOrFunction = Union[float, complex, np.ndarray, Tensor, Pwc, Stf]
_IntType = (int, np.integer)
