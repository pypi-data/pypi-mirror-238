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

import pandas as pd

AXES = ["index", "columns"]


def _get_implied_dimension_from_axes(records):
    return sum([axis.nlevels for axis in records.axes])


def _assert_axes_no_nans(records):
    for axis_name, axis in zip(AXES, records.axes):
        if isinstance(axis, pd.MultiIndex):
            for n in range(axis.nlevels):
                if axis.get_level_values(n).hasnans:
                    raise Exception(
                        f"Tabular 'records' cannot have missing index information (i.e., NaNs detected in `records.{axis_name}.get_level_values({n})`)"
                    )
        else:
            if axis.hasnans:
                raise Exception(
                    f"Tabular 'records' cannot have missing index information (i.e., NaNs detected in `records.{axis_name}`)"
                )


def _assert_axes_no_dups(records):
    for axis_name, axis in zip(AXES, records.axes):
        if isinstance(axis, pd.MultiIndex):
            for n in range(axis.nlevels):
                if axis.levels[n].has_duplicates:
                    raise Exception(
                        f"Tabular 'records' must have unique index information (i.e., duplicates detected in MultiIndex level: `records.{axis_name}.levels[{n}]`)"
                    )
        else:
            if axis.has_duplicates:
                raise Exception(
                    f"Tabular 'records' must have unique index information (i.e., duplicates detected in `records.{axis_name}`)"
                )


def _flatten_and_convert(records):
    dtypes = []
    for axis_name, axis in zip(AXES, records.axes):
        if isinstance(axis, pd.MultiIndex):
            # create empty dataframe to help build new MultiIndex
            mi = pd.DataFrame(columns=list(range(axis.nlevels)))

            for n in range(axis.nlevels):
                mi[n] = axis.get_level_values(n)

                if not isinstance(mi[n].dtype, pd.CategoricalDtype):
                    codes, cats = mi[n].factorize()
                    mi[n] = pd.Categorical(
                        values=codes, categories=cats, ordered=True, fastpath=True
                    )

                dtypes.append(mi[n].dtype)

            setattr(
                records,
                axis_name,
                pd.MultiIndex(
                    levels=[
                        pd.CategoricalIndex(
                            list(range(len(mi[n].cat.categories))), ordered=True
                        )
                        for n in mi.columns
                    ],
                    codes=[mi[n].cat.codes for n in mi.columns],
                ),
            )

        else:
            idx = axis.get_level_values(0)
            dtypes.append(pd.CategoricalDtype(idx, ordered=True))

            setattr(
                records,
                axis_name,
                pd.CategoricalIndex(list(range(len(idx))), ordered=True),
            )

    # stack (keeping  NaNs)
    if isinstance(records, pd.DataFrame):
        records = records.stack(
            list(range(records.columns.nlevels)), dropna=False
        ).reset_index(drop=False)
    else:
        records = records.reset_index(drop=False)

    # apply original categorical ordering
    for n, dtype in enumerate(dtypes):
        cats = dtype.categories.astype(str).tolist()
        records.isetitem(
            n,
            records.iloc[:, n].cat.set_categories(
                list(map(str.rstrip, cats)),
                rename=True,
                ordered=True,
            ),
        )

    return records
