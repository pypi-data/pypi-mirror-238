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

import os
import pathlib
from collections.abc import Iterable
import pandas as pd
from gams.control import GamsDatabase
from gams.core import gmd
from gams.transfer._internals import (
    SourceType,
    EQU_TYPE,
    TRANSFER_TO_GAMS_VARIABLE_SUBTYPES,
    TRANSFER_TO_GAMS_EQUATION_SUBTYPES,
)
import gams.transfer._abcs as abcs


class CCCMixin:
    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    def __len__(self):
        return len(self.data)

    def isValid(self, symbols=None, verbose=False, force=False):
        if not isinstance(symbols, (str, list, type(None))):
            raise TypeError("Argument 'symbols' must be type list or NoneType")

        if symbols is None:
            cache = True
            symbols = list(self.data.keys())
        else:
            cache = False

        if isinstance(symbols, str):
            symbols = [symbols]

        if isinstance(symbols, list):
            if any(not isinstance(i, str) for i in symbols):
                raise TypeError("Argument 'symbols' must contain only type str")

        if not isinstance(verbose, bool):
            raise ValueError("Argument 'verbose' must be type bool")

        if not isinstance(force, bool):
            raise ValueError("Argument 'force' must be type bool")

        if force:
            self._requires_state_check = True

        if self._requires_state_check:
            try:
                self._assert_is_valid(symbols)

                if not cache:
                    self._requires_state_check = True

                return True
            except Exception as err:
                if verbose:
                    raise err
                return False
        else:
            return True

    def listSymbols(self, is_valid=None):
        if not isinstance(is_valid, (bool, type(None))):
            raise TypeError("Argument 'is_valid' must be type bool or NoneType")

        if is_valid is True:
            return [symname for symname, symobj in self if symobj.isValid()]
        elif is_valid is False:
            return [symname for symname, symobj in self if not symobj.isValid()]
        else:
            return [symname for symname, symobj in self]

    def listParameters(self, is_valid=None):
        if not isinstance(is_valid, (bool, type(None))):
            raise TypeError("Argument 'is_valid' must be type bool or NoneType")

        return [
            symobj.name
            for symobj in self.getSymbols(self.listSymbols(is_valid))
            if isinstance(symobj, abcs.ABCParameter)
        ]

    def listSets(self, is_valid=None):
        if not isinstance(is_valid, (bool, type(None))):
            raise TypeError("Argument 'is_valid' must be type bool or NoneType")

        return [
            symobj.name
            for symobj in self.getSymbols(self.listSymbols(is_valid))
            if isinstance(symobj, abcs.ABCSet)
        ]

    def listAliases(self, is_valid=None):
        if not isinstance(is_valid, (bool, type(None))):
            raise TypeError("Argument 'is_valid' must be type bool or NoneType")

        return [
            symobj.name
            for symobj in self.getSymbols(self.listSymbols(is_valid))
            if isinstance(symobj, (abcs.ABCAlias, abcs.ABCUniverseAlias))
        ]

    def listVariables(self, is_valid=None, types=None):
        if not isinstance(is_valid, (bool, type(None))):
            raise TypeError("Argument 'is_valid' must be type bool or NoneType")

        if not isinstance(types, (str, list, type(None))):
            raise TypeError("Argument 'types' must be type str, list, or NoneType")

        if types is None:
            return [
                symobj.name
                for symobj in self.getSymbols(self.listSymbols(is_valid))
                if isinstance(symobj, abcs.ABCVariable)
            ]

        else:
            if isinstance(types, str):
                types = [types]

            # casefold to allow mixed case matching
            types = [i.casefold() for i in types]

            if any(i not in TRANSFER_TO_GAMS_VARIABLE_SUBTYPES.keys() for i in types):
                raise ValueError(
                    "User input unrecognized variable type, "
                    f"variable types can only take: {list(TRANSFER_TO_GAMS_VARIABLE_SUBTYPES.keys())}"
                )

            return [
                symobj.name
                for symobj in self.getSymbols(self.listSymbols(is_valid))
                if isinstance(symobj, abcs.ABCVariable) and symobj.type in types
            ]

    def listEquations(self, is_valid=None, types=None):
        if not isinstance(is_valid, (bool, type(None))):
            raise TypeError("Argument 'is_valid' must be type bool or NoneType")

        if not isinstance(types, (str, list, type(None))):
            raise TypeError("Argument 'types' must be type str, list, or NoneType")

        if types is None:
            return [
                symobj.name
                for symobj in self.getSymbols(self.listSymbols(is_valid))
                if isinstance(symobj, abcs.ABCEquation)
            ]

        else:
            if isinstance(types, str):
                types = [types]

            # casefold to allow mixed case matching (and extended syntax)
            types = [EQU_TYPE[i.casefold()] for i in types]

            if any(i not in TRANSFER_TO_GAMS_EQUATION_SUBTYPES.keys() for i in types):
                raise ValueError(
                    "User input unrecognized variable type, "
                    f"variable types can only take: {list(TRANSFER_TO_GAMS_EQUATION_SUBTYPES.keys())}"
                )

            return [
                symobj.name
                for symobj in self.getSymbols(self.listSymbols(is_valid))
                if isinstance(symobj, abcs.ABCEquation) and symobj.type in types
            ]

    def read(self, load_from, symbols=None, records=True, mode=None, encoding=None):
        if not isinstance(records, bool):
            raise TypeError("Argument 'records' must be type bool")

        if not isinstance(symbols, (list, str, type(None))):
            raise TypeError("Argument 'symbols' must be type str, list, or NoneType")

        if isinstance(symbols, str):
            symbols = [symbols]

        if symbols is not None:
            if any(not isinstance(i, str) for i in symbols):
                raise Exception("Argument 'symbols' must contain only type str")

        if mode is None:
            mode = "category"

        if not isinstance(mode, str):
            raise TypeError("Argument 'mode' must be type str (`string` or `category`)")

        if not isinstance(encoding, (str, type(None))):
            raise TypeError("Argument 'encoding' must be type str or NoneType")

        #
        # figure out data source type
        if isinstance(load_from, GamsDatabase):
            source = SourceType.GMD
            load_from = load_from._gmd

        elif isinstance(load_from, (os.PathLike, str)):
            fpath = pathlib.Path(load_from)

            if not fpath.expanduser().exists():
                raise Exception(
                    f"GDX file '{os.fspath(fpath.expanduser().resolve())}' does not exist, "
                    "check filename spelling or path specification"
                )

            if not os.fspath(fpath.expanduser().resolve()).endswith(".gdx"):
                raise Exception(
                    "Unexpected file type passed to 'load_from' argument "
                    "-- expected file extension '.gdx'"
                )

            source = SourceType.GDX
            load_from = os.fspath(fpath.expanduser().resolve())

        elif isinstance(load_from, abcs.ABCContainer):
            source = SourceType.CONTAINER

        else:
            # try GMD, if not, then mark as unknown
            try:
                ret = gmd.gmdInfo(load_from, gmd.GMD_NRSYMBOLSWITHALIAS)
                assert ret[0] == 1
                source = SourceType.GMD
            except:
                source = SourceType.UNKNOWN

        #
        # test for valid source
        if source is SourceType.UNKNOWN:
            raise TypeError(
                "Argument 'load_from' expects "
                "type str or PathLike (i.e., a path to a GDX file) "
                ", a valid gmdHandle (or GamsDatabase instance) "
                ", an instance of another Container "
                ", User passed: "
                f"'{type(load_from)}'."
            )

        #
        # read different types
        if source is SourceType.GDX:
            self._gdx_read(load_from, symbols, records, mode, encoding)

        elif source is SourceType.GMD:
            self._gmd_read(load_from, symbols, records, mode, encoding)

        elif source is SourceType.CONTAINER:
            self._container_read(load_from, symbols, records)

    def describeSets(self, symbols=None):
        if not isinstance(symbols, (str, list, type(None))):
            raise TypeError("Argument 'symbols' must be type str, list, or NoneType")

        if symbols is None:
            symbols = self.listSets()

        if isinstance(symbols, str):
            symbols = [symbols]

        if any(not isinstance(i, str) for i in symbols):
            raise TypeError("Argument 'symbols' must only contain type str")

        dfs = []
        cols = [
            "name",
            "is_singleton",
            "domain",
            "domain_type",
            "dimension",
            "number_records",
            "sparsity",
        ]

        # find all sets and aliases
        all_sets = self.listSets()
        all_aliases = self.listAliases()
        all_sets_aliases = all_sets + all_aliases

        data = []
        for i in symbols:
            if i in all_sets_aliases:
                data.append(
                    (
                        i,
                        self[i].is_singleton,
                        self[i].domain_names,
                        self[i].domain_type,
                        self[i].dimension,
                        self[i].number_records,
                        self[i].getSparsity(),
                    )
                )

        # create dataframe
        if data != []:
            df = pd.DataFrame(data, columns=cols)

            if any(i in all_aliases for i in symbols):
                df_is_alias = []
                df_alias_with = []

                for i in symbols:
                    if i in all_sets_aliases:
                        df_is_alias.append(
                            isinstance(self[i], (abcs.ABCAlias, abcs.ABCUniverseAlias))
                        )

                        if isinstance(self[i], abcs.ABCAlias):
                            df_alias_with.append(self[i].alias_with.name)
                        elif isinstance(self[i], abcs.ABCUniverseAlias):
                            df_alias_with.append(self[i].alias_with)
                        else:
                            df_alias_with.append(None)

                # add in is_alias column
                df.insert(2, "is_alias", pd.Series(df_is_alias, dtype=bool))
                df.insert(3, "alias_with", pd.Series(df_alias_with, dtype=object))

            return df.round(3).sort_values(by="name", ignore_index=True)
        else:
            return None

    def describeAliases(self, symbols=None):
        if not isinstance(symbols, (str, list, type(None))):
            raise TypeError("Argument 'symbols' must be type str, list, or NoneType")

        if symbols is None:
            symbols = self.listAliases()

        if isinstance(symbols, str):
            symbols = [symbols]

        if any(not isinstance(i, str) for i in symbols):
            raise TypeError("Argument 'symbols' must only contain type str")

        dfs = []
        cols = [
            "name",
            "alias_with",
            "is_singleton",
            "domain",
            "domain_type",
            "dimension",
            "number_records",
            "sparsity",
        ]

        # find aliases
        all_aliases = self.listAliases()

        data = []
        for i in symbols:
            if i in all_aliases:
                if isinstance(self[i], abcs.ABCAlias):
                    alias_name = self[i].alias_with.name
                elif isinstance(self[i], abcs.ABCUniverseAlias):
                    alias_name = self[i].alias_with
                else:
                    raise Exception("Encountered unknown symbol type")

                data.append(
                    (
                        i,
                        alias_name,
                        self[i].is_singleton,
                        self[i].domain_names,
                        self[i].domain_type,
                        self[i].dimension,
                        self[i].number_records,
                        self[i].getSparsity(),
                    )
                )

        if data != []:
            return (
                pd.DataFrame(data, columns=cols)
                .round(3)
                .sort_values(by="name", ignore_index=True)
            )
        else:
            return None

    def describeParameters(self, symbols=None):
        if not isinstance(symbols, (str, list, type(None))):
            raise TypeError("Argument 'symbols' must be type str, list, or NoneType")

        if symbols is None:
            symbols = self.listParameters()

        if isinstance(symbols, str):
            symbols = [symbols]

        if any(not isinstance(i, str) for i in symbols):
            raise TypeError("Argument 'symbols' must only contain type str")

        dfs = []
        cols = [
            "name",
            "domain",
            "domain_type",
            "dimension",
            "number_records",
            "min",
            "mean",
            "max",
            "where_min",
            "where_max",
            "sparsity",
        ]

        # find all parameters
        all_parameters = self.listParameters()

        data = []
        for i in symbols:
            if i in all_parameters:
                data.append(
                    (
                        i,
                        self[i].domain_names,
                        self[i].domain_type,
                        self[i].dimension,
                        self[i].number_records,
                        self[i].getMinValue(),
                        self[i].getMeanValue(),
                        self[i].getMaxValue(),
                        self[i].whereMin(),
                        self[i].whereMax(),
                        self[i].getSparsity(),
                    )
                )

        if data != []:
            return (
                pd.DataFrame(data, columns=cols)
                .round(3)
                .sort_values(by="name", ignore_index=True)
            )
        else:
            return None

    def describeVariables(self, symbols=None):
        if not isinstance(symbols, (str, list, type(None))):
            raise TypeError("Argument 'symbols' must be type str, list, or NoneType")

        if symbols is None:
            symbols = self.listVariables()

        if isinstance(symbols, str):
            symbols = [symbols]

        if any(not isinstance(i, str) for i in symbols):
            raise TypeError("Argument 'symbols' must only contain type str")

        dfs = []
        cols = [
            "name",
            "type",
            "domain",
            "domain_type",
            "dimension",
            "number_records",
            "sparsity",
            "min_level",
            "mean_level",
            "max_level",
            "where_max_abs_level",
        ]

        # find all variables
        all_variables = self.listVariables()

        data = []
        for i in symbols:
            if i in all_variables:
                data.append(
                    (
                        i,
                        self[i].type,
                        self[i].domain_names,
                        self[i].domain_type,
                        self[i].dimension,
                        self[i].number_records,
                        self[i].getSparsity(),
                        self[i].getMinValue("level"),
                        self[i].getMeanValue("level"),
                        self[i].getMaxValue("level"),
                        self[i].whereMaxAbs("level"),
                    )
                )
        if data != []:
            return (
                pd.DataFrame(data, columns=cols)
                .round(3)
                .sort_values(by="name", ignore_index=True)
            )
        else:
            return None

    def describeEquations(self, symbols=None):
        if not isinstance(symbols, (str, list, type(None))):
            raise TypeError("Argument 'symbols' must be type str, list, or NoneType")

        if symbols is None:
            symbols = self.listEquations()

        if isinstance(symbols, str):
            symbols = [symbols]

        if any(not isinstance(i, str) for i in symbols):
            raise TypeError("Argument 'symbols' must only contain type str")

        dfs = []
        cols = [
            "name",
            "type",
            "domain",
            "domain_type",
            "dimension",
            "number_records",
            "sparsity",
            "min_level",
            "mean_level",
            "max_level",
            "where_max_abs_level",
        ]

        # find all equations
        all_equations = self.listEquations()

        data = []
        for i in symbols:
            if i in all_equations:
                data.append(
                    (
                        i,
                        self[i].type,
                        self[i].domain_names,
                        self[i].domain_type,
                        self[i].dimension,
                        self[i].number_records,
                        self[i].getSparsity(),
                        self[i].getMinValue("level"),
                        self[i].getMeanValue("level"),
                        self[i].getMaxValue("level"),
                        self[i].whereMaxAbs("level"),
                    )
                )

        if data != []:
            return (
                pd.DataFrame(data, columns=cols)
                .round(3)
                .sort_values(by="name", ignore_index=True)
            )
        else:
            return None

    def getSets(self, is_valid=None):
        return self.getSymbols(self.listSets(is_valid=is_valid))

    def getAliases(self, is_valid=None):
        return self.getSymbols(self.listAliases(is_valid=is_valid))

    def getParameters(self, is_valid=None):
        return self.getSymbols(self.listParameters(is_valid=is_valid))

    def getVariables(self, is_valid=None, types=None):
        return self.getSymbols(self.listVariables(is_valid=is_valid, types=types))

    def getEquations(self, is_valid=None, types=None):
        return self.getSymbols(self.listEquations(is_valid=is_valid, types=types))

    def getSymbols(self, symbols=None):
        if symbols is None:
            return list(self.data.values())

        if isinstance(symbols, str):
            symbols = [symbols]

        if not isinstance(symbols, Iterable):
            raise ValueError("Argument 'symbols' must be type str or other iterable")

        obj = []
        for symname in symbols:
            try:
                obj.append(self[symname])
            except KeyError as err:
                raise KeyError(f"Symbol `{symname}` does not appear in the Container")
        return obj
