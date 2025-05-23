# Copyright 2024 The HuggingFace Team. All rights reserved.
# Copyright 2024 Intel Corporation. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import torch

from ..extension import Extension, register_extension


__all__ = []


module_path = os.path.dirname(__file__)
sources = [
    "unpack.sycl",
    "pybind_module.cpp",
]
ext = Extension(
    "quanto_xpu",
    root_dir=os.path.dirname(__file__),
    sources=sources,
)
register_extension(ext)


@torch.library.impl("quanto::unpack", "XPU")
def unpack_xpu(t: torch.Tensor, bits: int):
    return ext.lib.unpack(t, bits)
