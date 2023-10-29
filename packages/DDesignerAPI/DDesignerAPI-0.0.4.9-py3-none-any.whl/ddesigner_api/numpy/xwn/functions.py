# Copyright 2023 The Deeper-I Authors. All Rights Reserved.
#
# BSD 3-Clause License
# 
# Copyright (c) 2017, 
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# 
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# 
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# -*- coding: utf-8 -*-

import numpy as np


def _get_bit_map(bit:int, max_scale:float):
    map_scale = []
    for i in range(bit):
        coeff = np.power(0.5, i)
        map_scale.append((max_scale * coeff)[..., None])

    return np.concatenate(map_scale, axis=-1)


def get_sign(x, mode:str='hw'):
    if mode == 'hw':
        # Map of sign - Plus=False, Minus=True
        return x < 0.
    else: # mode == 'sw':
        return np.where(x >= 0., 1., -1.)
        

def get_magnitude(x, mask=None, kernel_axis:tuple=(0,1), method:str='L1'):
    # Magnitude
    if method =='L2':
        m = np.mean(np.sqrt(np.square(x)), axis=kernel_axis) # (i,o)
    elif method =='L1':
        m = np.mean(np.abs(x), axis=kernel_axis) # (i,o)
    else:
        m = np.mean(np.abs(x), axis=kernel_axis) # (i,o)
    
    if mask is not None:
        m *= mask

    return m

def get_scale(x, bit:int, max_scale:float, dtype:str='float32'):
    x_mag = get_magnitude(x)

    # No Scale bit
    if bit < 1:
        x_p = np.where((x >= 0.), x_mag, 0.) # (h,w,i,o)
        x_n = np.where((x < 0.), -x_mag, 0.) # (h,w,i,o)
        x = x_p + x_n
        indices = np.zeros(x, dtype=dtype)

    # Scale bit
    else:
        scale_map = _get_bit_map(2 ** (bit - 1), max_scale) * x_mag[..., None] # (i,o,bb)

        # Map of weight
        diff = np.abs(np.abs(x)[..., None] - scale_map)
        indices = np.argmin(diff, axis=-1)[..., None]
        map_x = np.ones_like(diff, dtype=dtype) * scale_map
        x = np.take_along_axis(map_x, indices, axis=-1)[..., 0]

    return x, indices.astype('uint8')


def get_header(w, use_pruning=False):
    _w = w.transpose().astype(np.float32) # (i,o) -> (o,i)
    in_shape = w.shape
    zero_cnt = 0
    w_1d = np.reshape(_w, (_w.size,))
    header_1d = np.zeros(w_1d.shape, dtype=np.uint8)
    for i in range(len(header_1d)):
        # Valid value
        if (w_1d[i] != 0.0) or (zero_cnt == 127):
            header_1d[i] = zero_cnt
            zero_cnt = 0
        # Last input channel element must get value
        elif (i > 0) and (((i+1)%in_shape[0]) == 0):
            header_1d[i] = zero_cnt
            zero_cnt = 0
        # Non-valid value(zero)
        else:
            header_1d[i] = 128
            zero_cnt += 1

    if not use_pruning:
        header_1d = np.zeros_like(header_1d, dtype=np.uint8)

    header = np.reshape(header_1d, in_shape).T
    return header

def find_bit_scale(x):
    u = np.unique(x[np.where(x != 0.)])
    return u.size, np.max(u) 


