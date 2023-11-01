#
# GAMS - General Algebraic Modeling System Python API
#
# Copyright (c) 2017-2023 GAMS Development Corp. <support@gams.com>
# Copyright (c) 2017-2023 GAMS Software GmbH <support@gams.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import itertools
import random
import numpy as np
import pandas as pd
import gams.transfer._abcs as abcs
from typing import Sequence


def check_all_same(iterable1: Sequence, iterable2: Sequence) -> bool:
    if len(iterable1) != len(iterable2):
        return False

    all_same = True
    for elem1, elem2 in zip(iterable1, iterable2):
        if elem1 is not elem2:
            return False
    return all_same


def get_keys_and_values(symobj, mode):
    if symobj.records is None:
        if isinstance(symobj, abcs.ABCSet):
            arrkeys = np.full((0, symobj.dimension), "", dtype=dtype_keys)
            arrvals = np.full((0, 1), "", dtype=object)
            return (arrkeys, arrvals)
        if isinstance(symobj, abcs.ABCParameter):
            arrkeys = np.full((0, symobj.dimension), "", dtype=dtype_keys)
            arrvals = np.full((0, len(symobj._attributes)), "", dtype=np.float64)
            return (arrkeys, arrvals)
        if isinstance(symobj, (abcs.ABCVariable, abcs.ABCEquation)):
            arrkeys = np.full((0, symobj.dimension), "", dtype=dtype_keys)
            arrvals = np.full((0, len(symobj._attributes)), "", dtype=np.float64)
            return (arrkeys, arrvals)

    else:
        #
        #
        # get keys array
        if mode == "string":
            nrecs = symobj.number_records
            if symobj.dimension == 0:
                arrkeys = np.array([[]], dtype=object)
            elif symobj.dimension == 1:
                arrkeys = np.empty(nrecs, dtype=object)
                arrkeys[:nrecs] = symobj.records[symobj.records.columns[0]]
                arrkeys = arrkeys.reshape((nrecs, 1), order="F")
            else:
                arrkeys = np.empty(symobj.dimension * nrecs, dtype=object)
                for i in range(symobj.dimension):
                    idx_start = i * nrecs
                    idx_end = i * nrecs + nrecs
                    arrkeys[idx_start:idx_end] = symobj.records[
                        symobj.records.columns[i]
                    ]

                arrkeys = arrkeys.reshape((nrecs, symobj.dimension), order="F")

        elif mode == "category":
            nrecs = symobj.number_records
            if symobj.dimension == 0:
                arrkeys = np.array([[]], dtype=int)
            elif symobj.dimension == 1:
                arrkeys = np.empty(nrecs, dtype=int)
                arrkeys[:nrecs] = symobj.records[symobj.records.columns[0]].cat.codes
                arrkeys = arrkeys.reshape((nrecs, 1), order="F")
            else:
                arrkeys = np.empty(symobj.dimension * nrecs, dtype=int)
                for i in range(symobj.dimension):
                    idx_start = i * nrecs
                    idx_end = i * nrecs + nrecs
                    arrkeys[idx_start:idx_end] = symobj.records[
                        symobj.records.columns[i]
                    ].cat.codes

                arrkeys = arrkeys.reshape((nrecs, symobj.dimension), order="F")
        else:
            raise ValueError("Unrecognized write 'mode'.")
        #
        #
        # get values array
        if symobj.dimension == 0:
            arrvals = symobj.records.to_numpy()
        else:
            if isinstance(symobj, (abcs.ABCSet, abcs.ABCParameter)):
                arrvals = (
                    symobj.records[symobj.records.columns[-1]]
                    .to_numpy()
                    .reshape((-1, 1))
                )
            else:
                arrvals = np.empty(len(symobj._attributes) * nrecs, dtype=np.float64)
                for i in range(len(symobj._attributes)):
                    idx_start = i * nrecs
                    idx_end = i * nrecs + nrecs
                    arrvals[idx_start:idx_end] = symobj.records[
                        symobj.records.columns[i + symobj.dimension]
                    ].to_numpy()

                arrvals = arrvals.reshape((nrecs, len(symobj._attributes)), order="F")

        return (arrkeys, arrvals)


def convert_to_categoricals_str(arrkeys, arrvals, all_uels):
    has_domains = arrkeys.size > 0
    has_values = arrvals.size > 0

    dfs = []
    if has_domains:
        dfs.append(pd.DataFrame(arrkeys))

    if has_values:
        dfs.append(pd.DataFrame(arrvals))

    if has_domains and has_values:
        df = pd.concat(dfs, axis=1, copy=False)
        df.columns = pd.RangeIndex(start=0, stop=len(df.columns))
    elif has_domains or has_values:
        df = dfs[0]
        df.columns = pd.RangeIndex(start=0, stop=len(df.columns))
    else:
        df = None

    if has_domains:
        rk, ck = arrkeys.shape
        for i in range(ck):
            dtype = pd.CategoricalDtype(categories=all_uels, ordered=True)
            df.isetitem(
                i, pd.Categorical(values=df[i], dtype=dtype).remove_unused_categories()
            )

    return df


def convert_to_categoricals_cat(arrkeys, arrvals, unique_uels):
    has_domains = arrkeys.size > 0
    has_values = arrvals.size > 0

    dfs = []
    if has_domains:
        dfs.append(pd.DataFrame(arrkeys))

    if has_values:
        dfs.append(pd.DataFrame(arrvals))

    if has_domains and has_values:
        df = pd.concat(dfs, axis=1, copy=False)
        df.columns = pd.RangeIndex(start=0, stop=len(df.columns))
    elif has_domains or has_values:
        df = dfs[0]
        df.columns = pd.RangeIndex(start=0, stop=len(df.columns))
    else:
        df = None

    if has_domains:
        rk, ck = arrkeys.shape
        for i in range(ck):
            dtype = pd.CategoricalDtype(categories=unique_uels[i], ordered=True)
            df.isetitem(i, pd.Categorical(values=df[i], dtype=dtype, fastpath=True))

    return df


def generate_unique_labels(labels):
    if not isinstance(labels, list):
        labels = [labels]

    # default domain labels
    labels = [i if i != "*" else "uni" for i in labels]

    # make unique
    is_unique = False
    if len(labels) == len(set(labels)):
        is_unique = True

    if not is_unique:
        labels = [f"{i}_{n}" for n, i in enumerate(labels)]

    return labels


def cartesian_product(*arrays):
    la = len(arrays)
    dtype = np.result_type(*arrays)
    arr = np.empty((la, *map(len, arrays)), dtype=dtype)
    idx = slice(None), *itertools.repeat(None, la)
    for i, a in enumerate(arrays):
        arr[i, ...] = a[idx[: la - i]]
    return arr.reshape(la, -1).T


def choice_no_replace(choose_from, n_choose, seed=None):
    if not isinstance(seed, (int, type(None))):
        raise TypeError("Argument 'seed' must be type int or NoneType")

    if not isinstance(choose_from, int):
        choose_from = int(choose_from)

    if not isinstance(n_choose, int):
        n_choose = int(n_choose)

    density = n_choose / choose_from

    try:
        if density == 1:
            return np.arange(choose_from, dtype=int)

        # numpy is faster as density grows
        if 0.08 < density < 1:
            rng = np.random.default_rng(seed)
            idx = rng.choice(
                np.arange(choose_from, dtype=int), replace=False, size=(n_choose,)
            )

        # random.shuffle is much much faster at low density
        elif density <= 0.08:
            random.seed(seed)
            idx = np.array(random.sample(range(choose_from), n_choose), dtype=int)
        else:
            raise Exception(
                "Argument 'density' is our of bounds, must be on the interval [0,1]."
            )

        return np.sort(idx)

    except Exception as err:
        raise err
