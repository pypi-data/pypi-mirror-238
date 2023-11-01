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

import numpy as np
from gams.transfer._internals import SpecialValues
import gams.transfer._abcs as abcs


class PVEMixin:
    @property
    def shape(self):
        if self.domain_type == "regular":
            return tuple(
                [
                    0
                    if i.getUELs(0, ignore_unused=True) is None
                    else len(i.getUELs(0, ignore_unused=True))
                    for i in self.domain
                ]
            )
        else:
            return tuple(
                [
                    0
                    if self.getUELs(i, ignore_unused=True) is None
                    else len(self.getUELs(i, ignore_unused=True))
                    for i in range(self.dimension)
                ]
            )

    @property
    def is_scalar(self):
        return self.dimension == 0

    def findEps(self, column=None):
        return self.findSpecialValues(SpecialValues.EPS, column=column)

    def findNA(self, column=None):
        return self.findSpecialValues(SpecialValues.NA, column=column)

    def findUndef(self, column=None):
        return self.findSpecialValues(SpecialValues.UNDEF, column=column)

    def findPosInf(self, column=None):
        return self.findSpecialValues(SpecialValues.POSINF, column=column)

    def findNegInf(self, column=None):
        return self.findSpecialValues(SpecialValues.NEGINF, column=column)

    def findSpecialValues(self, values, column=None):
        # ARG: values
        if not isinstance(values, (float, list)):
            raise TypeError("Argument 'values' must be type float or list")

        if isinstance(values, float):
            values = [values]

        for i in values:
            if not (
                SpecialValues.isEps(i)
                or SpecialValues.isNA(i)
                or SpecialValues.isUndef(i)
                or SpecialValues.isPosInf(i)
                or SpecialValues.isNegInf(i)
            ):
                return ValueError(
                    "Argument 'values' is currently limited to one of the "
                    "five special value constants defined as: "
                    "EPS, NA, UNDEF, POSINF, or NEGINF"
                )

        # ARG: columns
        # set defaults
        if column is None:
            if isinstance(self, abcs.ABCParameter):
                column = "value"
            elif isinstance(self, (abcs.ABCVariable, abcs.ABCEquation)):
                column = "level"
            else:
                raise Exception(f"Unsupported object type: {type(self)}")

        # checks
        if not isinstance(column, str):
            raise TypeError(
                f"Argument 'column' must be type str. User passed {type(column)}."
            )

        if column not in self._attributes:
            raise TypeError(
                f"Argument 'column' must be a one of the following: {self._attributes}"
            )

        if self.records is not None:
            for n, i in enumerate(values):
                if n == 0:
                    if SpecialValues.isEps(i):
                        idx = SpecialValues.isEps(self.records[column])
                    elif SpecialValues.isNA(i):
                        idx = SpecialValues.isNA(self.records[column])
                    elif SpecialValues.isUndef(i):
                        idx = SpecialValues.isUndef(self.records[column])
                    elif SpecialValues.isPosInf(i):
                        idx = SpecialValues.isPosInf(self.records[column])
                    elif SpecialValues.isNegInf(i):
                        idx = SpecialValues.isNegInf(self.records[column])
                    else:
                        raise Exception("Unknown special value detected")
                else:
                    if SpecialValues.isEps(i):
                        idx = (idx) | (SpecialValues.isEps(self.records[column]))
                    elif SpecialValues.isNA(i):
                        idx = (idx) | (SpecialValues.isNA(self.records[column]))
                    elif SpecialValues.isUndef(i):
                        idx = (idx) | (SpecialValues.isUndef(self.records[column]))
                    elif SpecialValues.isPosInf(i):
                        idx = (idx) | (SpecialValues.isPosInf(self.records[column]))
                    elif SpecialValues.isNegInf(i):
                        idx = (idx) | (SpecialValues.isNegInf(self.records[column]))
                    else:
                        raise Exception("Unknown special value detected")

            return self.records.loc[idx, :]

    def countNA(self, columns=None):
        return self._countSpecialValues(SpecialValues.NA, columns=columns)

    def countEps(self, columns=None):
        return self._countSpecialValues(SpecialValues.EPS, columns=columns)

    def countUndef(self, columns=None):
        return self._countSpecialValues(SpecialValues.UNDEF, columns=columns)

    def countPosInf(self, columns=None):
        return self._countSpecialValues(SpecialValues.POSINF, columns=columns)

    def countNegInf(self, columns=None):
        return self._countSpecialValues(SpecialValues.NEGINF, columns=columns)

    def _countSpecialValues(self, special_value, columns):
        # ARG: special_value
        if not isinstance(special_value, float):
            raise TypeError("Argument 'float' must be type float")

        if not (
            SpecialValues.isEps(special_value)
            or SpecialValues.isNA(special_value)
            or SpecialValues.isUndef(special_value)
            or SpecialValues.isPosInf(special_value)
            or SpecialValues.isNegInf(special_value)
        ):
            return ValueError(
                "Argument 'special_value' is currently limited to one of the "
                "five special value constants defined as: "
                "SpecialValues.EPS SpecialValues.NA, SpecialValues.UNDEF, "
                "SpecialValues.POSINF, or SpecialValues.NEGINF"
            )

        # ARG: columns
        # set defaults
        if columns is None:
            if isinstance(self, abcs.ABCParameter):
                columns = "value"
            elif isinstance(self, (abcs.ABCVariable, abcs.ABCEquation)):
                columns = "level"
            else:
                raise Exception(f"Unsupported object type: {type(self)}")

        # checks
        if not isinstance(columns, (str, list)):
            raise TypeError(
                f"Argument 'columns' must be type str or list. User passed {type(columns)}."
            )

        if isinstance(columns, str):
            columns = [columns]

        if any(not isinstance(i, str) for i in columns):
            raise TypeError(f"Argument 'columns' must contain only type str.")

        if any(i not in self._attributes for i in columns):
            raise TypeError(
                f"Argument 'columns' must be a subset of the following: {self._attributes}"
            )

        if self.records is not None:
            if SpecialValues.isEps(special_value):
                return np.sum(SpecialValues.isEps(self.records[columns]))
            elif SpecialValues.isNA(special_value):
                return np.sum(SpecialValues.isNA(self.records[columns]))
            elif SpecialValues.isUndef(special_value):
                return np.sum(SpecialValues.isUndef(self.records[columns]))
            elif SpecialValues.isPosInf(special_value):
                return np.sum(SpecialValues.isPosInf(self.records[columns]))
            elif SpecialValues.isNegInf(special_value):
                return np.sum(SpecialValues.isNegInf(self.records[columns]))
            else:
                raise Exception("Unknown special value detected")

    def whereMax(self, column=None):
        return self._whereMetric("max", column=column)

    def whereMaxAbs(self, column=None):
        return self._whereMetric("absmax", column=column)

    def whereMin(self, column=None):
        return self._whereMetric("min", column=column)

    def _whereMetric(self, metric, column):
        # ARG: metric
        if not isinstance(metric, str):
            raise TypeError("Argument 'metric' must be type str")

        if metric not in [
            "max",
            "min",
            "absmax",
        ]:
            return ValueError(
                "Argument 'metric' is currently limited to str type 'max', 'min' or 'absmax'"
            )

        # ARG: columns

        # set defaults
        if column is None:
            if isinstance(self, abcs.ABCParameter):
                column = "value"
            elif isinstance(self, (abcs.ABCVariable, abcs.ABCEquation)):
                column = "level"
            else:
                raise Exception(f"Unsupported object type: {type(self)}")

        # checks
        if not isinstance(column, str):
            raise TypeError(
                f"Argument 'column' must be type str. User passed {type(column)}."
            )

        if column not in self._attributes:
            raise TypeError(
                f"Argument 'column' must be a one of the following: {self._attributes}"
            )

        if self.records is not None:
            dom = []
            if metric == "max":
                if self.dimension > 0:
                    try:
                        dom = list(
                            self.records[
                                self.records[column] == self.getMaxValue(column)
                            ].to_numpy()[0][: self.dimension]
                        )
                        return dom
                    except Exception as err:
                        return None

            if metric == "min":
                if self.dimension > 0:
                    try:
                        dom = list(
                            self.records[
                                self.records[column] == self.getMinValue(column)
                            ].to_numpy()[0][: self.dimension]
                        )
                        return dom
                    except:
                        return None

            if metric == "absmax":
                if self.dimension > 0:
                    try:
                        dom = list(
                            self.records[
                                self.records[column] == self.getMaxAbsValue(column)
                            ].to_numpy()[0][: self.dimension]
                        )
                        return dom
                    except:
                        return None

    def getMaxValue(self, columns=None):
        return self._getMetric(metric="max", columns=columns)

    def getMinValue(self, columns=None):
        return self._getMetric(metric="min", columns=columns)

    def getMeanValue(self, columns=None):
        return self._getMetric(metric="mean", columns=columns)

    def getMaxAbsValue(self, columns=None):
        return self._getMetric(metric="absmax", columns=columns)

    def _getMetric(self, metric, columns):
        # ARG: metric
        if not isinstance(metric, str):
            raise TypeError("Argument 'metric' must be type str")

        if metric not in [
            "max",
            "min",
            "mean",
            "absmax",
        ]:
            return ValueError(
                "Argument 'metric' is currently limited to str type 'max', 'min' or 'mean', absmax"
            )

        # ARG: columns
        # set defaults
        if columns is None:
            if isinstance(self, abcs.ABCParameter):
                columns = "value"
            elif isinstance(self, (abcs.ABCVariable, abcs.ABCEquation)):
                columns = "level"

        # checks
        if not isinstance(columns, (str, list)):
            raise TypeError(
                f"Argument 'columns' must be type str or list. User passed {type(columns)}."
            )

        if isinstance(columns, str):
            columns = [columns]

        if any(not isinstance(i, str) for i in columns):
            raise TypeError(f"Argument 'columns' must contain only type str.")

        if any(i not in self._attributes for i in columns):
            raise TypeError(
                f"Argument 'columns' must be a subset of the following: {self._attributes}"
            )

        if self.records is not None:
            if metric == "max":
                return self.records[columns].max().max()
            elif metric == "min":
                return self.records[columns].min().min()
            elif metric == "mean":
                if not (
                    self.records[columns].min().min() == float("-inf")
                    and self.records[columns].max().max() == float("inf")
                ):
                    return self.records[columns].mean().mean()
                else:
                    return float("nan")
            elif metric == "absmax":
                return self.records[columns].abs().max().max()
