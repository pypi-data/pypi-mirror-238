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

import copy
import itertools
import pandas as pd
from pandas.api.types import (
    CategoricalDtype,
    infer_dtype,
)
import numpy as np
from gams.core import gdx
from gams.transfer._abcs import ABCParameter, ABCSet, ABCContainer
from gams.transfer.syms._mixins import PVEMixin, SAPVEMixin, SAUAPVEMixin, SPVEMixin
from gams.transfer._internals import (
    generate_unique_labels,
    cartesian_product,
    EPS,
    SpecialValues,
    UNDEF,
    NA,
)

from gams.transfer.syms._mixins.pivot import PivotParameterMixin
from gams.transfer.syms._mixins.generateRecords import GenerateRecordsParameterMixin
from gams.transfer.syms._mixins.equals import EqualsParameterMixin
from typing import Any, Optional, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from gams.transfer import Container

try:
    from scipy.sparse import coo_matrix

    scipy_available = True
except:
    scipy_available = False


class Parameter(
    PVEMixin,
    SAPVEMixin,
    SAUAPVEMixin,
    SPVEMixin,
    PivotParameterMixin,
    GenerateRecordsParameterMixin,
    EqualsParameterMixin,
    ABCParameter,
):
    @classmethod
    def _from_gams(cls, container, name, domain, records=None, description=""):
        # create new symbol object
        obj = Parameter.__new__(cls)

        # set private properties directly
        obj._requires_state_check = False
        obj._container = container
        container._requires_state_check = True
        obj._name = name
        obj._domain = domain
        obj._domain_forwarding = False
        obj._description = description
        obj._records = records
        obj._modified = True

        # typing
        obj._gams_type = gdx.GMS_DT_PAR
        obj._gams_subtype = 0

        # add to container
        container.data.update({name: obj})

        return obj

    def __new__(cls, *args, **kwargs):
        if len(args) == 0:
            return object.__new__(Parameter)

        try:
            symobj = args[0][args[1]]
        except:
            symobj = None

        if symobj is None:
            return object.__new__(Parameter)
        else:
            if isinstance(symobj, ABCParameter):
                return symobj
            else:
                raise TypeError(
                    f"Cannot overwrite symbol `{symobj.name}` in container because it is not a Parameter object)"
                )

    def __init__(
        self,
        container: "Container",
        name: str,
        domain: Optional[list] = None,
        records: Optional[Any] = None,
        domain_forwarding: bool = False,
        description: str = "",
        uels_on_axes: bool = False,
    ):
        """Parameter symbol

        Parameters
        ----------
        container : Container
        name : str
        domain : list, optional
        records : Any, optional
        domain_forwarding : bool, optional
        description : str, optional

        Example
        ----------
        >>> m = gt.Container()
        >>> i = gt.Set(m, "i", records=['i1','i2'])
        >>> a = gt.Parameter(m, "a", [i], records=[['i1',1],['i2',2]])
        """
        # domain handling
        if domain is None:
            domain = []

        if isinstance(domain, (ABCSet, str)):
            domain = [domain]

        # does symbol exist
        has_symbol = False
        if isinstance(getattr(self, "container", None), ABCContainer):
            has_symbol = True

        if has_symbol:
            try:
                if any(
                    d1 != d2 for d1, d2 in itertools.zip_longest(self.domain, domain)
                ):
                    raise ValueError(
                        "Cannot overwrite symbol in container unless symbol domains are equal"
                    )

                if self.domain_forwarding != domain_forwarding:
                    raise ValueError(
                        "Cannot overwrite symbol in container unless 'domain_forwarding' is left unchanged"
                    )

            except ValueError as err:
                raise ValueError(err)

            except TypeError as err:
                raise TypeError(err)

            # reset some properties
            self._requires_state_check = True
            self.container._requires_state_check = True
            if description != "":
                self.description = description
            self.records = None
            self.modified = True

            # only set records if records are provided
            if records is not None:
                self.setRecords(records, uels_on_axes=uels_on_axes)

        else:
            # populate new symbol properties
            self._requires_state_check = True
            self.container = container
            self.container._requires_state_check = True
            self.name = name
            self.domain = domain
            self.domain_forwarding = domain_forwarding
            self.description = description
            self.records = None
            self.modified = True

            # typing
            self._gams_type = gdx.GMS_DT_PAR
            self._gams_subtype = 0

            # only set records if records are provided
            if records is not None:
                self.setRecords(records, uels_on_axes=uels_on_axes)

            # add to container
            container.data.update({name: self})

    def __repr__(self):
        return f"<Parameter `{self.name}` ({hex(id(self))})>"

    def __delitem__(self):
        del self.container.data[self.name]

    @property
    def _attributes(self):
        return ["value"]

    @property
    def summary(self):
        return {
            "name": self.name,
            "description": self.description,
            "domain": self.domain_names,
            "domain_type": self.domain_type,
            "dimension": self.dimension,
            "number_records": self.number_records,
        }

    def toValue(self):
        from gams.transfer.syms._methods.toValue import toValueParameter

        if not self.isValid():
            raise Exception(
                f"Cannot extract value because `{self.name}` is not a valid symbol object. "
                f"Use `{self.name}.isValid(verbose=True)` to debug."
            )

        return toValueParameter(self)

    def toList(self):
        from gams.transfer.syms._methods.toList import toListParameter

        if not self.isValid():
            raise Exception(
                f"Cannot extract list because `{self.name}` is not a valid symbol object. "
                f"Use `{self.name}.isValid(verbose=True)` to debug."
            )
        return toListParameter(self)

    def toDict(self, orient=None):
        from gams.transfer.syms._methods.toDict import toDictParameter

        if not self.isValid():
            raise Exception(
                f"Cannot extract dict because `{self.name}` is not a valid symbol object. "
                f"Use `{self.name}.isValid(verbose=True)` to debug."
            )

        return toDictParameter(self, orient=orient)

    def dropZeros(self):
        mask = (self.records.iloc[:, -1] == 0.0) & (
            ~SpecialValues.isEps(self.records.iloc[:, -1])
        )
        self.records = self.records.loc[~mask, :].reset_index(drop=True)

    def dropDefaults(self):
        self.dropZeros()

    def dropEps(self):
        mask = pd.Series(SpecialValues.isEps(self.records.iloc[:, -1]), dtype=bool)
        self.records = self.records[~mask].reset_index(drop=True)

    def dropNA(self):
        mask = pd.Series(SpecialValues.isNA(self.records.iloc[:, -1]), dtype=bool)
        self.records = self.records[~mask].reset_index(drop=True)

    def dropUndef(self):
        mask = pd.Series(SpecialValues.isUndef(self.records.iloc[:, -1]), dtype=bool)
        self.records = self.records[~mask].reset_index(drop=True)

    def dropMissing(self):
        mask = pd.Series(pd.isna(self.records.iloc[:, -1]), dtype=bool)
        self.records = self.records[~mask].reset_index(drop=True)

    def setRecords(self, records: Any, uels_on_axes=False):
        if not isinstance(uels_on_axes, bool):
            raise TypeError("Argument 'uels_on_axes' must be type bool.")

        if isinstance(records, (int, float)):
            self._from_int_float(records)

        elif isinstance(records, np.ndarray):
            self._from_ndarray(records)

        elif isinstance(records, pd.DataFrame):
            self._from_dataframe(records, uels_on_axes=uels_on_axes)

        elif isinstance(records, pd.Series):
            self._from_series(records)

        else:
            self._from_else(records)

    def _from_series(self, records: pd.Series):
        from gams.transfer.syms._methods.tables import (
            _assert_axes_no_nans,
            _assert_axes_no_dups,
            _get_implied_dimension_from_axes,
            _flatten_and_convert,
        )

        records = copy.deepcopy(records)

        # check if index has NaNs
        try:
            _assert_axes_no_nans(records)
        except Exception as err:
            raise err

        # check if index has duplicates
        try:
            _assert_axes_no_dups(records)
        except Exception as err:
            raise err

        # check dimensionality of data
        if self.is_scalar:
            if records.size == 1:
                records = pd.DataFrame(records)
                self._from_dataframe(records)

            else:
                raise Exception(
                    f"Attempting to set records for a scalar symbol but records.size > 1. "
                    "pandas.Series must have size exactly = 1 before setting records. "
                    "(Note: pandas.Series.index is ignored for scalar symbols)"
                )

        else:
            dim = _get_implied_dimension_from_axes(records)
            if dim != self.dimension:
                raise Exception(
                    f"Dimensionality of data ({dim}) is inconsistent "
                    f"with domain specification ({self.dimension})"
                )

            # flatten and convert to categorical
            records = _flatten_and_convert(records)

            # remap special values (str -> float)
            records = self._remap_str_special_values(records)

            # convert data column to type float
            if not isinstance(records.iloc[:, -1].dtype, float):
                records.isetitem(-1, records.iloc[:, -1].astype(float))

            # reset columns
            records.columns = (
                generate_unique_labels(self.domain_names) + self._attributes
            )

            # set records
            self.records = records

    def _from_dataframe(self, records: pd.DataFrame, uels_on_axes: bool = False):
        if self.is_scalar:
            self._from_flat_dataframe(records)

        else:
            if uels_on_axes:
                self._from_table_dataframe(records)
            else:
                self._from_flat_dataframe(records)

    def _from_flat_dataframe(self, records: pd.DataFrame):
        records = pd.DataFrame(copy.deepcopy(records))

        # check dimensionality of data
        r, c = records.shape
        if c - 1 != self.dimension:
            raise Exception(
                f"Dimensionality of records ({c - 1}) is inconsistent "
                f"with parameter domain specification ({self.dimension})"
            )

        if self.is_scalar and r > 1:
            raise Exception(
                f"Attempting to set {r} records for a scalar symbol. "
                f"Must define a domain for symbol `{self.name}` in order to set multiple records."
            )

        # keep user defined categories if provided
        for i in range(self.dimension):
            # create categorical
            if not isinstance(records.iloc[:, i].dtype, CategoricalDtype):
                records.isetitem(
                    i,
                    records.iloc[:, i].astype(
                        CategoricalDtype(
                            categories=records.iloc[:, i].unique(),
                            ordered=True,
                        )
                    ),
                )

            # capture user categories
            old_cats = records.iloc[:, i].cat.categories.tolist()
            is_ordered = records.iloc[:, i].cat.ordered

            # convert any non-str categories to str, strip trailing white-space and de-dup
            new_cats = list(dict.fromkeys(list(map(str.rstrip, map(str, old_cats)))))

            # if categories are not unique after strip then need to remake the categorical
            if len(old_cats) != len(new_cats):
                # convert data to str, strip white-space and make categorical
                records.isetitem(
                    i,
                    records.iloc[:, i]
                    .astype(str)
                    .map(str.rstrip)
                    .astype(CategoricalDtype(categories=new_cats, ordered=is_ordered)),
                )

            else:
                # only need to rename the categories
                records.isetitem(i, records.iloc[:, i].cat.rename_categories(new_cats))

        # remap special values (str -> float)
        records = self._remap_str_special_values(records)

        # convert data column to type float if needed
        if not isinstance(records.iloc[:, -1].dtype, float):
            records.isetitem(-1, records.iloc[:, -1].astype(float))

        # reset columns
        records.columns = (
            generate_unique_labels(records.columns[: self.dimension].tolist())
            + self._attributes
        )

        # set records
        self.records = records

    def _from_table_dataframe(self, records: pd.DataFrame):
        from gams.transfer.syms._methods.tables import (
            _assert_axes_no_nans,
            _assert_axes_no_dups,
            _get_implied_dimension_from_axes,
            _flatten_and_convert,
        )

        records = pd.DataFrame(copy.deepcopy(records))

        # check if index has NaNs
        try:
            _assert_axes_no_nans(records)
        except Exception as err:
            raise err

        # check if index has duplicates
        try:
            _assert_axes_no_dups(records)
        except Exception as err:
            raise err

        # check dimensionality of data
        dim = _get_implied_dimension_from_axes(records)
        if dim != self.dimension:
            raise Exception(
                f"Dimensionality of table ({dim}) is inconsistent "
                f"with parameter domain specification ({self.dimension})"
            )

        # flatten and convert to categorical
        records = _flatten_and_convert(records)

        # remap special values (str -> float)
        records = self._remap_str_special_values(records)

        # convert data column to type float
        if not isinstance(records.iloc[:, -1].dtype, float):
            records.isetitem(-1, records.iloc[:, -1].astype(float))

        # reset column names
        records.columns = generate_unique_labels(self.domain_names) + self._attributes

        # set records
        self._records = records

    def _from_int_float(self, records: Union[int, float]):
        if not self.is_scalar:
            raise Exception(
                "Attempting to set a record with a scalar value, however the "
                "symbol is not currently defined as a scalar (i.e., <symbol>.is_scalar == False)"
            )

        # note we do not drop zeros when setting
        records = pd.DataFrame([records], dtype=float, columns=self._attributes)

        # set records
        self._records = records

    def _from_ndarray(self, records: np.ndarray):
        try:
            records = np.array(records, dtype=float)
        except Exception as err:
            raise Exception(
                f"Attempted conversion to numpy array (dtype=float) failed. Reason {err}"
            )

        # user flexibility for (n,1) and (1,n) arrays (auto reshape)
        if self.dimension == 1 and (
            records.shape == (1, records.size) or records.shape == (records.size, 1)
        ):
            records = records.reshape((records.size,))

        # check dimension of array and symbol
        if records.ndim != self.dimension:
            raise Exception(
                f"Attempting to set records for a {self.dimension}-dimensional "
                f"symbol with a numpy array that is {records.ndim}-dimensional "
                "-- array reshape necessary. (Note: gams.transfer will auto "
                "reshape array if symbol is 1D and array is either (1,n) or (n,1))"
            )

        # records must have regular domain_type if not a scalar
        if records.ndim > 0 and self.domain_type != "regular":
            raise Exception(
                "Data conversion for non-scalar array (i.e., matrix) format into "
                "records is only possible for symbols where "
                "self.domain_type = `regular`. "
                "Must define symbol with specific domain set objects, "
                f"symbol domain_type is currently `{self.domain_type}`."
            )

        # make sure array has the proper shape
        if records.shape != self.shape:
            raise Exception(
                f"User passed array with shape `{records.shape}` but anticipated "
                f"shape was `{self.shape}` based "
                "on domain set information -- "
                "must reconcile before array-to-records conversion is possible."
            )

        # check that all domains are valid
        for i in self.domain:
            if not i.isValid():
                raise Exception(
                    f"Domain set `{i.name}` is invalid and cannot "
                    "be used to convert array-to-records.  "
                    "Use `<symbol>.isValid(verbose=True)` to debug "
                    "this domain set symbol before proceeding."
                )

        # create array of codes
        codes = [np.arange(len(d.getUELs(ignore_unused=True))) for d in self.domain]

        # create dataframe
        if self.is_scalar:
            df = pd.DataFrame(index=[0])
        else:
            df = pd.DataFrame(cartesian_product(*tuple(codes)))

            # create categoricals
            for n, d in enumerate(self.domain):
                dtype = CategoricalDtype(
                    categories=d.records.iloc[:, 0].cat.categories,
                    ordered=d.records.iloc[:, 0].cat.ordered,
                )

                df.isetitem(
                    n, pd.Categorical.from_codes(codes=df.iloc[:, n], dtype=dtype)
                )

        # insert matrix elements
        df["value"] = records.reshape(-1, 1)

        # drop zeros and reset index
        df = self._filter_zero_records(df)

        # reset column names
        df.columns = generate_unique_labels(self.domain_names) + self._attributes

        # set records
        self.records = df

    def _from_else(self, records: Any):
        try:
            records = pd.DataFrame(records)
        except Exception as err:
            raise Exception(
                "Data structure passed as argument 'records' could not be "
                f"successfully converted into a pandas DataFrame (reason: {err})."
            )

        # check dimensionality of data
        r, c = records.shape
        if c - 1 != self.dimension:
            raise Exception(
                f"Dimensionality of records ({c - 1}) is inconsistent "
                f"with parameter domain specification ({self.dimension})"
            )

        if self.is_scalar and r > 1:
            raise Exception(
                f"Attempting to set {r} values for a scalar symbol. "
                f"Must define a domain for symbol `{self.name}` in order to set multiple records."
            )

        # keep user defined categories if provided
        for i in range(self.dimension):
            # create categorical
            if not isinstance(records.iloc[:, i].dtype, CategoricalDtype):
                records.isetitem(
                    i,
                    records.iloc[:, i].astype(
                        CategoricalDtype(
                            categories=records.iloc[:, i].unique(),
                            ordered=True,
                        )
                    ),
                )

            # capture user categories
            old_cats = records.iloc[:, i].cat.categories.tolist()
            is_ordered = records.iloc[:, i].cat.ordered

            # convert any non-str categories to str, strip trailing white-space and de-dup
            new_cats = list(dict.fromkeys(list(map(str.rstrip, map(str, old_cats)))))

            # if categories are not unique after strip then need to remake the categorical
            if len(old_cats) != len(new_cats):
                # convert data to str, strip white-space and make categorical
                records.isetitem(
                    i,
                    records.iloc[:, i]
                    .astype(str)
                    .map(str.rstrip)
                    .astype(CategoricalDtype(categories=new_cats, ordered=is_ordered)),
                )

            else:
                # only need to rename the categories
                records.isetitem(i, records.iloc[:, i].cat.rename_categories(new_cats))

        # remap special values
        records = self._remap_str_special_values(records)

        # convert data column to type float if needed
        if records.iloc[:, -1].dtype != float:
            records.isetitem(-1, records.iloc[:, -1].astype(float))

        # reset columns
        records.columns = generate_unique_labels(self.domain_names) + self._attributes

        # set records
        self.records = records

    def toSparseCoo(self):
        if not scipy_available:
            raise ModuleNotFoundError(
                f"Module 'scipy' was not found -- sparse "
                "data output is only possible if 'scipy' has been installed"
            )

        if not self.isValid():
            raise Exception(
                "Cannot create sparse array (i.e., coo_matrix) because symbol "
                "is invalid -- use `<symbol>.isValid(verbose=True)` to debug symbol state."
            )
        if self.domain_type == "regular":
            if self.hasDomainViolations():
                raise Exception(
                    "Cannot create sparse array because there are domain violations "
                    "(i.e., UELs in the symbol are not a subset of UELs contained in domain sets)."
                )

        if self.records is not None:
            if self.is_scalar:
                row = [0]
                col = [0]
                m = 1
                n = 1

            elif self.dimension == 1:
                if self.domain_type == "regular":
                    col = (
                        self.records.iloc[:, 0]
                        .map(self.domain[0]._getUELCodes(0, ignore_unused=True))
                        .to_numpy(dtype=int)
                    )
                else:
                    col = self.records.iloc[:, 0].cat.codes.to_numpy(dtype=int)

                row = np.zeros(len(col), dtype=int)
                m, *n = self.shape
                assert n == []
                n = m
                m = 1

            elif self.dimension == 2:
                if self.domain_type == "regular":
                    row = (
                        self.records.iloc[:, 0]
                        .map(self.domain[0]._getUELCodes(0, ignore_unused=True))
                        .to_numpy(dtype=int)
                    )
                    col = (
                        self.records.iloc[:, 1]
                        .map(self.domain[1]._getUELCodes(0, ignore_unused=True))
                        .to_numpy(dtype=int)
                    )
                else:
                    row = self.records.iloc[:, 0].cat.codes.to_numpy(dtype=int)
                    col = self.records.iloc[:, 1].cat.codes.to_numpy(dtype=int)

                m, n = self.shape
            else:
                raise Exception(
                    "Sparse coo_matrix formats are only "
                    "available for data that has dimension <= 2"
                )

            return coo_matrix(
                (self.records.iloc[:, -1].to_numpy(dtype=float), (row, col)),
                shape=(m, n),
                dtype=float,
            )
        else:
            return None

    def toDense(self):
        if not self.isValid():
            raise Exception(
                "Cannot create dense array (i.e., matrix) format because symbol "
                "is invalid -- use `<symbol>.isValid(verbose=True)` to debug symbol state."
            )

        if self.records is not None:
            if self.is_scalar:
                return self.records.to_numpy(dtype=float).reshape(self.shape)
            else:
                #
                #
                # checks
                if self.domain_type == "regular":
                    if self.hasDomainViolations():
                        raise Exception(
                            "Cannot create dense array because there are domain violations "
                            "(i.e., UELs in the symbol are not a subset of UELs contained in domain sets)."
                        )

                    # check order of domain UELs in categorical and order of domain UELs in data
                    for symobj in self.domain:
                        data_cats = symobj.records.iloc[:, 0].unique().tolist()
                        cats = symobj.records.iloc[:, 0].cat.categories.tolist()

                        if data_cats != cats[: len(data_cats)]:
                            raise Exception(
                                f"`toDense` requires that UEL data order of domain set `{symobj.name}` must be "
                                "equal be equal to UEL category order (i.e., the order that set elements "
                                "appear in rows of the dataframe and the order set elements are specified by the categorical). "
                                "Users can efficiently reorder their domain set UELs to data order with "
                                "the `reorderUELs()` method (no arguments) -- preexisting unused categories "
                                "will be appended (maintaining their order)."
                            )
                else:
                    # check order of domain UELs in categorical and order of domain UELs in data
                    for n in range(self.dimension):
                        # check if any invalid codes
                        if any(
                            code == -1 for code in self.records.iloc[:, n].cat.codes
                        ):
                            raise Exception(
                                f"Invalid category detected in dimension `{n}` (code == -1), "
                                "cannot create array until all categories are properly resolved"
                            )

                        data_cats = self.records.iloc[:, n].unique().tolist()
                        cats = self.records.iloc[:, n].cat.categories.tolist()

                        if data_cats != cats[: len(data_cats)]:
                            raise Exception(
                                f"`toDense` requires (for 'relaxed' symbols) that UEL data order must be "
                                "equal be equal to UEL category order (i.e., the order that set elements "
                                "appear in rows of the dataframe and the order set elements are specified by the categorical). "
                                "Users can efficiently reorder UELs to data order with "
                                "the `reorderUELs()` method (no arguments) -- preexisting unused categories "
                                "will be appended (maintaining their order)."
                            )

                #
                #
                # create indexing scheme
                if self.domain_type == "regular":
                    idx = [
                        self.records.iloc[:, n]
                        .map(domainobj._getUELCodes(0, ignore_unused=True))
                        .to_numpy(dtype=int)
                        for n, domainobj in enumerate(self.domain)
                    ]

                else:
                    idx = [
                        self.records.iloc[:, n].cat.codes.to_numpy(dtype=int)
                        for n, domainobj in enumerate(self.domain)
                    ]

                # fill the dense array
                a = np.zeros(self.shape)
                val = self.records.iloc[:, -1].to_numpy(dtype=float)
                a[tuple(idx)] = val

                return a
        else:
            return None

    def _remap_str_special_values(self, records):
        # convert str "eps", "na", & "undef" special value strings to float equivalents
        if infer_dtype(records.iloc[:, -1]) not in [
            "integer",
            "floating",
            "mixed-integer-float",
        ]:
            idx = records.iloc[:, -1].isin(EPS)
            if idx.any():
                records.loc[
                    records[idx].index,
                    records.columns[-1],
                ] = SpecialValues.EPS

            idx = records.iloc[:, -1].isin(UNDEF)
            if idx.any():
                records.loc[
                    records[idx].index,
                    records.columns[-1],
                ] = SpecialValues.UNDEF

            idx = records.iloc[:, -1].isin(NA)
            if idx.any():
                records.loc[
                    records[idx].index,
                    records.columns[-1],
                ] = SpecialValues.NA

        return records

    def _filter_zero_records(self, records):
        idx = (records.iloc[:, -1] == 0.0) & (~SpecialValues.isEps(records.iloc[:, -1]))
        return records.loc[~idx, :].reset_index(drop=True)
