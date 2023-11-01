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

from warnings import warn
import pandas as pd
import numpy as np
from pandas.api.types import (
    CategoricalDtype,
    is_float_dtype,
    infer_dtype,
)
import gams.transfer._abcs as abcs
from gams.transfer._internals import (
    GAMS_MAX_INDEX_DIM,
    GAMS_DESCRIPTION_MAX_LENGTH,
    DomainStatus,
    DomainViolation,
    generate_unique_labels,
)


class SPVEMixin:
    def __delitem__(self):
        # TODO: add in some functionality that might relax the symbols down to a different domain
        #       This function would mimic the <Container>.removeSymbols() method -- is more pythonic
        del self.container.data[self.name]

    @property
    def domain_forwarding(self):
        return self._domain_forwarding

    @domain_forwarding.setter
    def domain_forwarding(self, domain_forwarding):
        if not isinstance(domain_forwarding, (bool, list)):
            raise TypeError("Argument 'domain_forwarding' must be type bool or list")

        if isinstance(domain_forwarding, list):
            if len(domain_forwarding) != self.dimension:
                raise Exception(
                    "Argument 'domain_forwarding' must be of length <symbol>.dimension"
                )

            if any(not isinstance(i, bool) for i in domain_forwarding):
                raise TypeError(
                    "Argument 'domain_forwarding' must only contain type bool"
                )

        self._domain_forwarding = domain_forwarding
        self.modified = True
        self.container.modified = True

    @property
    def domain_names(self):
        return [
            i.name if isinstance(i, abcs.AnyContainerDomainSymbol) else i
            for i in self.domain
        ]

    @property
    def domain_labels(self):
        if self._records is not None:
            return self._records.columns.tolist()[: self.dimension]

    @domain_labels.setter
    def domain_labels(self, labels):
        if not isinstance(labels, list):
            labels = [labels]

        # checks
        if len(labels) != self.dimension:
            raise Exception(
                "Attempting to set symbol 'domain_labels', however, len(domain_labels) != symbol dimension."
            )

        # make unique labels if necessary
        labels = generate_unique_labels(labels)

        # set the domain_labels
        if getattr(self, "domain_labels", None) is not None:
            if self._records.columns.tolist() != labels + self._attributes:
                self._records.columns = labels + self._attributes
                self._container._requires_state_check = True
                self._requires_state_check = True
                self.modified = True

    @property
    def domain(self):
        return self._domain

    @domain.setter
    def domain(self, domain):
        if not isinstance(domain, list):
            domain = [domain]

        if not all(isinstance(i, (abcs.AnyContainerDomainSymbol, str)) for i in domain):
            raise TypeError(
                "All 'domain' elements must be type Set, Alias, UniverseAlias, or str"
            )

        if any(
            getattr(i, "is_singleton", False)
            for i in domain
            if isinstance(i, abcs.AnyContainerDomainSymbol)
        ):
            raise Exception(
                "Singleton sets cannot be used to set the domain of a symbol"
            )

        if not all(
            i.dimension == 1
            for i in domain
            if isinstance(i, abcs.AnyContainerDomainSymbol)
        ):
            raise ValueError("All linked 'domain' elements must have dimension == 1")

        if len(domain) > GAMS_MAX_INDEX_DIM:
            raise ValueError(f"Symbol 'domain' length cannot be > {GAMS_MAX_INDEX_DIM}")

        # check to see if domain is being changed
        if getattr(self, "domain", None) is not None:
            if self.domain != domain:
                self._requires_state_check = True
                self.modified = True

                self.container._requires_state_check = True
                self.container.modified = True

                self._domain = domain
        else:
            self._domain = domain

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        if not isinstance(description, str):
            raise TypeError("Symbol 'description' must be type str")

        if len(description) > GAMS_DESCRIPTION_MAX_LENGTH:
            raise TypeError(
                f"Symbol 'description' must have "
                f"length {GAMS_DESCRIPTION_MAX_LENGTH} or smaller"
            )

        # check to see if _description is being changed
        if getattr(self, "description", None) is not None:
            if self.description != description:
                self._requires_state_check = True
                self.modified = True

                self.container._requires_state_check = True
                self.container.modified = True

        # set the description
        self._description = description

    @property
    def dimension(self):
        return len(self.domain)

    @dimension.setter
    def dimension(self, dimension):
        if not isinstance(dimension, int) or dimension < 0:
            raise TypeError(
                "Symbol 'dimension' must be type int (greater than or equal to 0)"
            )

        if dimension > GAMS_MAX_INDEX_DIM:
            raise ValueError(f"Symbol 'dimension' cannot be > {GAMS_MAX_INDEX_DIM}")

        if len(self.domain) > dimension:
            self.domain = [i for n, i in enumerate(self.domain) if n < dimension]
            self.modified = True
        elif dimension > len(self.domain):
            new = self.domain
            new.extend(["*"] * (dimension - len(self.domain)))
            self.domain = new
            self.modified = True
            self.container.modified = True
        else:
            pass

    @property
    def records(self):
        return self._records

    @records.setter
    def records(self, records):
        # set records
        self._records = records

        self._requires_state_check = True
        self.modified = True

        self.container._requires_state_check = True
        self.container.modified = True

        if self._records is not None:
            if self.domain_forwarding:
                self._domainForwarding()

                # reset state check flags for all symbols in the container
                for symnam, symobj in self.container.data.items():
                    symobj._requires_state_check = True

    @property
    def number_records(self):
        if self.isValid():
            if self.records is not None:
                return len(self.records)
            else:
                return 0
        else:
            return float("nan")

    def _getUELCodes(self, dimension, ignore_unused=False):
        if not isinstance(dimension, int):
            raise TypeError("Argument 'dimension' must be type int")

        if dimension >= self.dimension:
            raise ValueError(
                f"Argument 'dimension' (`{dimension}`) must be < symbol "
                f"dimension (`{self.dimension}`). (NOTE: 'dimension' is indexed from zero)"
            )

        if not isinstance(ignore_unused, bool):
            raise TypeError("Argument 'ignore_unused' must be type bool")

        cats = self.getUELs(dimension, ignore_unused=ignore_unused)
        codes = list(range(len(cats)))
        return dict(zip(cats, codes))

    def getUELs(
        self, dimensions=None, codes=None, ignore_unused=False, unique_only=False
    ):
        if self.records is not None:
            if not self.isValid():
                raise Exception(
                    "Symbol is currently invalid -- must be valid in order to access UELs (categories)."
                )

            # fastpath for scalars
            if self.dimension == 0:
                return []

            # ARG: ignore_unused
            if not isinstance(ignore_unused, bool):
                raise TypeError(f"Argument 'ignore_unused' must be type bool")

            # ARG: unique_only
            if not isinstance(unique_only, bool):
                raise TypeError(f"Argument 'unique_only' must be type bool")

            # ARG: dimension
            if not isinstance(dimensions, (list, int, type(None))):
                raise TypeError("Argument 'dimensions' must be type int or NoneType")

            if dimensions is None:
                dimensions = list(range(self.dimension))

            if isinstance(dimensions, int):
                dimensions = [dimensions]

            if any(not isinstance(i, int) for i in dimensions):
                raise TypeError("Argument 'dimensions' must only contain type int")

            for n in dimensions:
                if n >= self.dimension:
                    raise ValueError(
                        f"Cannot access symbol 'dimension' `{n}`, because `{n}` is >= symbol "
                        f"dimension (`{self.dimension}`). (NOTE: symbol 'dimension' is indexed from zero)"
                    )

            # ARG: codes
            if not isinstance(codes, (int, list, type(None))):
                raise TypeError("Argument 'codes' must be type int, list, or NoneType")

            if isinstance(codes, int):
                codes = [codes]

            if isinstance(codes, list):
                if any(not isinstance(i, int) for i in codes):
                    raise TypeError("Argument 'codes' must only contain type int")

            # ARG: codes & dimensions
            if codes is not None and dimensions is None:
                raise Exception(
                    "User must specify 'dimensions' if retrieving UELs with the 'codes' argument."
                )

            if codes is not None and len(dimensions) > 1:
                raise Exception(
                    "User must specify only one dimension if retrieving UELs with the 'codes' argument"
                )

            if codes is None:
                if len(dimensions) == 1:
                    n = dimensions[0]
                    if not ignore_unused:
                        cats = self.records.iloc[:, n].cat.categories.tolist()
                    else:
                        used_codes = np.sort(self.records.iloc[:, n].cat.codes.unique())
                        all_cats = self.records.iloc[:, n].cat.categories.tolist()
                        cats = [all_cats[i] for i in used_codes]
                elif len(dimensions) > 1:
                    cats = {}
                    for n in dimensions:
                        if not ignore_unused:
                            cats.update(
                                dict.fromkeys(self.records.iloc[:, n].cat.categories)
                            )
                        else:
                            used_codes = np.sort(
                                self.records.iloc[:, n].cat.codes.unique()
                            )
                            all_cats = self.records.iloc[:, n].cat.categories.tolist()
                            cats.update(
                                dict.fromkeys([all_cats[i] for i in used_codes])
                            )

                    cats = list(cats.keys())

                if unique_only:
                    return list(CasePreservingDict().fromkeys(cats.keys()).keys())
                else:
                    return cats

            else:
                codemap = {
                    codes: cats
                    for cats, codes in self._getUELCodes(dimensions[0]).items()
                }

                if len(codes) == 1:
                    codes = codes[0]
                    return codemap[codes]

                return [codemap.get(code, None) for code in codes]

    def _formatUELs(self, method, dimensions=None):
        if self.records is not None:
            if not self.isValid():
                raise Exception(
                    "Symbol is currently invalid -- must be valid in order to access UELs (categories)."
                )

            # ARG: dimension
            if not isinstance(dimensions, (list, int, type(None))):
                raise TypeError("Argument 'dimensions' must be type int or NoneType")

            if dimensions is None:
                dimensions = list(range(self.dimension))

            if isinstance(dimensions, int):
                dimensions = [dimensions]

            if any(not isinstance(i, int) for i in dimensions):
                raise TypeError("Argument 'dimensions' must only contain type int")

            for n in dimensions:
                if n >= self.dimension:
                    raise ValueError(
                        f"Cannot access symbol 'dimension' `{n}`, because `{n}` is >= symbol "
                        f"dimension (`{self.dimension}`). (NOTE: symbol 'dimension' is indexed from zero)"
                    )

            for n in dimensions:
                old_cats = self.records.iloc[:, n].cat.categories.tolist()
                new_cats = list(map(method, self.records.iloc[:, n].cat.categories))

                try:
                    # fastpath
                    self.records.isetitem(
                        n, self.records.iloc[:, n].cat.rename_categories(new_cats)
                    )
                except:
                    # remap data (slow path)
                    self.records.isetitem(
                        n,
                        self.records.iloc[:, n]
                        .astype("object")
                        .map(dict(zip(old_cats, new_cats))),
                    )

                    # de-dup new cats
                    new_cats = list(dict.fromkeys(new_cats).keys())

                    # rebuild categorical
                    self.records.isetitem(
                        n,
                        self.records.iloc[:, n].astype(
                            pd.CategoricalDtype(categories=new_cats, ordered=True)
                        ),
                    )

    def lowerUELs(self, dimensions=None):
        self._formatUELs(str.lower, dimensions=dimensions)
        return self

    def upperUELs(self, dimensions=None):
        self._formatUELs(str.upper, dimensions=dimensions)
        return self

    def lstripUELs(self, dimensions=None):
        self._formatUELs(str.lstrip, dimensions=dimensions)
        return self

    def rstripUELs(self, dimensions=None):
        self._formatUELs(str.rstrip, dimensions=dimensions)
        return self

    def stripUELs(self, dimensions=None):
        self._formatUELs(str.strip, dimensions=dimensions)
        return self

    def capitalizeUELs(self, dimensions=None):
        self._formatUELs(str.capitalize, dimensions=dimensions)
        return self

    def casefoldUELs(self, dimensions=None):
        self._formatUELs(str.casefold, dimensions=dimensions)
        return self

    def titleUELs(self, dimensions=None):
        self._formatUELs(str.title, dimensions=dimensions)
        return self

    def ljustUELs(self, length, fill_character=None, dimensions=None):
        if fill_character is None:
            fill_character = " "

        if fill_character == " ":
            warn(
                "Trailing spaces are not significant in GAMS, they will be dropped "
                "automatically if written to GAMS data structures (GDX/GMD). "
                "They are maintained if using generating other data formats (CSV, SQL, etc.)"
            )

        try:
            self._formatUELs(
                lambda x: x.ljust(length, fill_character), dimensions=dimensions
            )
        except Exception as err:
            raise Exception(
                f"Could not successfully left justify (ljust) categories in `{self.name}`. Reason: {err}"
            )

        return self

    def rjustUELs(self, length, fill_character=None, dimensions=None):
        if fill_character is None:
            fill_character = " "

        try:
            self._formatUELs(
                lambda x: x.rjust(length, fill_character), dimensions=dimensions
            )
        except Exception as err:
            raise Exception(
                f"Could not successfully right justify (rjust) categories in `{self.name}`. Reason: {err}"
            )

        return self

    def renameUELs(self, uels, dimensions=None, allow_merge=False):
        if self.records is not None:
            if not self.isValid():
                raise Exception(
                    "Symbol is currently invalid -- must be valid in order to access UELs (categories)."
                )

            #
            # ARG: uels
            if not isinstance(uels, (dict, list, str)):
                raise TypeError("Argument 'uels' must be type str, list, or dict")

            if isinstance(uels, str):
                uels = [uels]

            if isinstance(uels, dict):
                if any(
                    not isinstance(k, str) or not isinstance(v, str)
                    for k, v in uels.items()
                ):
                    raise TypeError(
                        "Argument 'uels' dict must have both keys and values "
                        "that are type str (i.e., {'<old uel name>':'<new uel name>'})"
                    )

                # trim all trailing whitespace
                uels = {k: v.rstrip() for k, v in uels.items()}

            if isinstance(uels, list):
                if any(not isinstance(i, str) for i in uels):
                    raise TypeError("Argument 'uels' must contain only type str")

                # trim all trailing whitespace
                uels = list(map(str.rstrip, uels))

            #
            # ARG: dimensions
            if not isinstance(dimensions, (int, list, type(None))):
                raise TypeError(
                    "Argument 'dimensions' must be type int, list, or NoneType"
                )

            if dimensions is None:
                dimensions = list(range(self.dimension))

            if isinstance(dimensions, int):
                dimensions = [dimensions]

            if any(not isinstance(i, int) for i in dimensions):
                raise TypeError("Argument 'dimensions' must only contain type int")

            for i in dimensions:
                if i >= self.dimension:
                    raise ValueError(
                        f"Cannot access symbol 'dimension' `{i}`, because `{i}` is >= symbol "
                        f"dimension (`{self.dimension}`). (NOTE: symbol 'dimension' is indexed from zero)"
                    )

            #
            # ARG: allow_merge
            if not isinstance(allow_merge, bool):
                raise TypeError("Argument 'allow_merge' must be type bool")

            #
            # check if uels has right length
            if isinstance(uels, list):
                for n in dimensions:
                    if len(uels) != len(self.records.iloc[:, n].cat.categories):
                        raise Exception(
                            f"Could not rename UELs (categories) in `{self.name}` dimension `{n}`. "
                            "Reason: new categories need to have the same "
                            "number of items as the old categories!"
                        )

            for n in dimensions:
                if allow_merge:
                    if isinstance(uels, list):
                        uel_map = dict(
                            zip(
                                self.records.iloc[:, n].cat.categories.tolist(),
                                uels,
                            )
                        )
                    else:
                        uel_map = uels

                    if any(
                        uel in self.records.iloc[:, n].cat.categories
                        for uel in uel_map.keys()
                    ):
                        is_ordered = self.records.iloc[:, n].dtype.ordered
                        old_uels = self.records.iloc[:, n].cat.categories.to_list()

                        # create and de-duplicate new_uels
                        new_uels = list(
                            dict.fromkeys(
                                [
                                    uel_map[uel] if uel in uel_map.keys() else uel
                                    for uel in old_uels
                                ]
                            )
                        )

                        # convert dimension back to object and do the string renaming

                        self.records.isetitem(
                            n,
                            self.records.iloc[:, n]
                            .astype("object")
                            .map(uel_map)
                            .fillna(self.records.iloc[:, n]),
                        )

                        # recreate the categorical
                        self.records.isetitem(
                            n,
                            self.records.iloc[:, n].astype(
                                CategoricalDtype(
                                    categories=new_uels, ordered=is_ordered
                                )
                            ),
                        )

                        self.modified = True
                        self.container.modified = True

                else:
                    try:
                        self.records.isetitem(
                            n, self.records.iloc[:, n].cat.rename_categories(uels)
                        )

                        self.modified = True
                        self.container.modified = True

                    except Exception as err:
                        raise Exception(
                            f"Could not rename UELs (categories) in `{self.name}` dimension `{n}`. Reason: {err}"
                        )

    def removeUELs(self, uels=None, dimensions=None):
        if self.records is not None:
            if not self.isValid():
                raise Exception(
                    "Symbol is currently invalid -- must be valid in order to access UELs (categories)."
                )

            # ARG: uels
            if not isinstance(uels, (list, str, type(None))):
                raise TypeError("Argument 'uels' must be type list, str for NoneType")

            if isinstance(uels, str):
                uels = [uels]

            if isinstance(uels, list):
                if any(not isinstance(i, str) for i in uels):
                    raise TypeError("Argument 'uels' must contain only type str")

            # ARG: dimensions
            if not isinstance(dimensions, (int, list, type(None))):
                raise TypeError(
                    "Argument 'dimensions' must be type int, list, or NoneType"
                )

            if dimensions is None:
                dimensions = list(range(self.dimension))

            if isinstance(dimensions, int):
                dimensions = [dimensions]

            if any(not isinstance(i, int) for i in dimensions):
                raise TypeError("Argument 'dimensions' must only contain type int")

            for i in dimensions:
                if i >= self.dimension:
                    raise ValueError(
                        f"Cannot access symbol 'dimension' `{i}`, because `{i}` is >= symbol "
                        f"dimension (`{self.dimension}`). (NOTE: symbol 'dimension' is indexed from zero)"
                    )

            # method body
            if uels is None:
                for n in dimensions:
                    try:
                        self.records.isetitem(
                            n, self.records.iloc[:, n].cat.remove_unused_categories()
                        )

                        self.modified = True
                        self.container.modified = True

                    except Exception as err:
                        raise Exception(
                            f"Could not remove unused UELs (categories) in symbol "
                            f"dimension `{n}`. Reason: {err}"
                        )
            else:
                for n in dimensions:
                    try:
                        self.records.isetitem(
                            n,
                            self.records.iloc[:, n].cat.remove_categories(
                                self.records.iloc[:, n].cat.categories.intersection(
                                    set(uels)
                                )
                            ),
                        )

                        self.modified = True
                        self.container.modified = True

                    except Exception as err:
                        raise Exception(
                            f"Could not remove unused UELs (categories) in symbol "
                            f"dimension `{n}`. Reason: {err}"
                        )

    def setUELs(self, uels, dimensions=None, rename=False):
        if self.records is not None:
            if not self.isValid():
                raise Exception(
                    "Symbol is currently invalid -- must be valid in order to set UELs (categories)."
                )

            # ARG: uels
            if not isinstance(uels, (str, list)):
                raise TypeError("Argument 'uels' must be type list or str")

            if isinstance(uels, str):
                uels = [uels]

            if any(not isinstance(uel, str) for uel in uels):
                raise TypeError("Argument 'uels' must only contain type str")

            # trim all trailing whitespace
            uels = list(map(str.rstrip, uels))

            # ARG: dimensions
            if not isinstance(dimensions, (int, list, type(None))):
                raise TypeError(
                    "Argument 'dimensions' must be type int, list, or NoneType"
                )

            if dimensions is None:
                dimensions = list(range(self.dimension))

            if isinstance(dimensions, int):
                dimensions = [dimensions]

            if any(not isinstance(i, int) for i in dimensions):
                raise TypeError("Argument 'dimensions' must only contain type int")

            for i in dimensions:
                if i >= self.dimension:
                    raise ValueError(
                        f"Cannot access symbol 'dimension' `{i}`, because `{i}` is >= symbol "
                        f"dimension (`{self.dimension}`). (NOTE: symbol 'dimension' is indexed from zero)"
                    )

            # ARG: rename
            if not isinstance(rename, bool):
                raise TypeError("Argument 'rename' must be type bool")

            for n in dimensions:
                try:
                    self.records.isetitem(
                        n,
                        self.records.iloc[:, n].cat.set_categories(
                            uels, ordered=True, rename=rename
                        ),
                    )

                    self.modified = True
                    self.container.modified = True

                except Exception as err:
                    raise Exception(
                        f"Could not set UELs (categories) in symbol dimension `{n}`. Reason: {err}"
                    )

    def reorderUELs(self, uels=None, dimensions=None):
        if self.records is not None:
            if not self.isValid():
                raise Exception(
                    "Symbol is currently invalid -- must be valid in order to reorder UELs (categories)."
                )

            # ARG: uels
            if not isinstance(uels, (str, list, type(None))):
                raise TypeError("Argument 'uels' must be type list, str, or NoneType")

            if isinstance(uels, str):
                uels = [uels]

            if uels is not None:
                if any(not isinstance(uel, str) for uel in uels):
                    raise TypeError("Argument 'uels' must only contain type str")

            # ARG: dimensions
            if not isinstance(dimensions, (int, list, type(None))):
                raise TypeError(
                    "Argument 'dimensions' must be type int, list, or NoneType"
                )

            if dimensions is None:
                dimensions = list(range(self.dimension))

            if isinstance(dimensions, int):
                dimensions = [dimensions]

            if any(not isinstance(i, int) for i in dimensions):
                raise TypeError("Argument 'dimensions' must only contain type int")

            for i in dimensions:
                if i >= self.dimension:
                    raise ValueError(
                        f"Cannot access symbol 'dimension' `{i}`, because `{i}` is >= symbol "
                        f"dimension (`{self.dimension}`). (NOTE: symbol 'dimension' is indexed from zero)"
                    )

            if uels is not None:
                for n in dimensions:
                    try:
                        # fastpath
                        self.records.isetitem(
                            n,
                            self.records.iloc[:, n].cat.reorder_categories(uels),
                        )

                    except:
                        # need to reset categories
                        try:
                            self.records.isetitem(n, self.setUELs(uels, dimensions=n))
                            self.modified = True
                            self.container.modified = True

                        except Exception as err:
                            raise Exception(
                                f"Could not reorder UELs (categories) in symbol dimension `{n}`. Reason: {err}"
                            )
            else:
                for n in dimensions:
                    old_cats = dict.fromkeys(self.records.iloc[:, n].cat.categories)
                    new_cats = dict.fromkeys(self.records.iloc[:, n].unique())

                    uels = new_cats
                    uels.update(dict.fromkeys(old_cats))
                    uels = list(uels.keys())

                    try:
                        # fastpath
                        self.records.isetitem(
                            n,
                            self.records.iloc[:, n].cat.reorder_categories(uels),
                        )

                    except:
                        # need to reset categories
                        try:
                            self.records.isetitem(n, self.setUELs(uels, dimensions=n))
                            self.modified = True
                            self.container.modified = True

                        except Exception as err:
                            raise Exception(
                                f"Could not reorder UELs (categories) in symbol dimension `{n}`. Reason: {err}"
                            )

    def addUELs(self, uels, dimensions=None):
        if self.records is not None:
            if not self.isValid():
                raise Exception(
                    "Symbol is currently invalid -- must be valid in order to access UELs (categories)."
                )

            # ARG: uels
            if not isinstance(uels, (str, list)):
                raise TypeError("Argument 'uels' must be type list or str")

            if isinstance(uels, str):
                uels = [uels]

            if any(not isinstance(uel, str) for uel in uels):
                raise TypeError("Argument 'uels' must only contain type str")

            # trim all trailing whitespace
            uels = list(map(str.rstrip, uels))

            # ARG: dimensions
            if not isinstance(dimensions, (int, list, type(None))):
                raise TypeError(
                    "Argument 'dimensions' must be type int, list, or NoneType"
                )

            if dimensions is None:
                dimensions = list(range(self.dimension))

            if isinstance(dimensions, int):
                dimensions = [dimensions]

            if any(not isinstance(i, int) for i in dimensions):
                raise TypeError("Argument 'dimensions' must only contain type int")

            for i in dimensions:
                if i >= self.dimension:
                    raise ValueError(
                        f"Cannot access symbol 'dimension' `{i}`, because `{i}` is >= symbol "
                        f"dimension (`{self.dimension}`). (NOTE: symbol 'dimension' is indexed from zero)"
                    )

            for n in dimensions:
                try:
                    self.records.isetitem(
                        n, self.records.iloc[:, n].cat.add_categories(uels)
                    )

                    self.modified = True
                    self.container.modified = True

                except Exception as err:
                    raise Exception(
                        f"Could not add UELs (categories) to symbol dimension `{n}`. Reason: {err}"
                    )

    def getDomainViolations(self):
        if self.records is None:
            return None

        else:
            dvobjs = []
            for n, symobj in enumerate(self.domain):
                if isinstance(symobj, abcs.AnyContainerDomainSymbol):
                    if not symobj.isValid():
                        raise Exception(
                            f"Cannot locate domain violations for symbol `{self.name}` "
                            f"because the referenced domain set `{symobj.name}` is not valid"
                        )

                    self_elem = pd.Series(self.getUELs(n, ignore_unused=True))

                    # domain violations are generated for all elements if the domain set does not have records
                    if symobj.records is not None:
                        domain_elem = pd.Series(symobj.getUELs(ignore_unused=True))
                    else:
                        domain_elem = pd.Series([])

                    idx = ~self_elem.map(str.casefold).isin(
                        domain_elem.map(str.casefold)
                    )

                    if any(idx):
                        dvobjs.append(
                            DomainViolation(self, n, symobj, self_elem[idx].tolist())
                        )

            if len(dvobjs) != 0:
                return dvobjs

    def findDomainViolations(self):
        if self.records is not None:
            violations = self.getDomainViolations()

            if violations is not None:
                for n, v in enumerate(violations):
                    set_v = set(v.violations)
                    if n == 0:
                        idx = self.records.iloc[:, v.dimension].isin(set_v)
                    else:
                        idx = (idx) | (self.records.iloc[:, v.dimension].isin(set_v))

                return self.records.loc[idx, :]
            else:
                return self.records.loc[pd.Index([]), :]

    def hasDomainViolations(self):
        if self.records is not None:
            return self.findDomainViolations().empty is False
        else:
            return 0

    def countDomainViolations(self):
        if self.records is not None:
            return len(self.findDomainViolations())
        else:
            return 0

    def dropDomainViolations(self):
        try:
            self.records.drop(index=self.findDomainViolations().index, inplace=True)
        except:
            return None

    def countDuplicateRecords(self):
        try:
            return len(self.findDuplicateRecords())
        except:
            return 0

    def findDuplicateRecords(self, keep="first"):
        if keep not in {"first", "last", False}:
            raise ValueError(
                "Argument 'keep' must be either 'first' "
                "(returns duplicates except for the first occurrence), "
                "'last' (returns duplicates except for the last occurrence), "
                "or False (returns all duplicates)"
            )

        # create a temporary copy
        df2 = self.records.copy()

        # casefold all domains
        for i in range(self.dimension):
            df2.isetitem(i, df2.iloc[:, i].map(str.casefold))

        idx = df2.duplicated(subset=df2.columns[: self.dimension], keep=keep)

        return self.records.loc[idx, :]

    def hasDuplicateRecords(self):
        return self.countDuplicateRecords() != 0

    def dropDuplicateRecords(self, keep="first"):
        try:
            self.records.drop(index=self.findDuplicateRecords(keep).index, inplace=True)
        except:
            return None

    @property
    def domain_type(self):
        return self._domain_status.name

    @property
    def _domain_status(self):
        if (
            all(isinstance(i, abcs.AnyContainerDomainSymbol) for i in self.domain)
            and self.dimension != 0
        ):
            return DomainStatus.regular
        elif all(i == "*" for i in self.domain):
            return DomainStatus.none
        elif self.dimension == 0:
            return DomainStatus.none
        else:
            return DomainStatus.relaxed

    def _domainForwarding(self):
        if isinstance(self.container, abcs.ABCContainer):
            if isinstance(self.domain_forwarding, bool):
                forwarding = [self.domain_forwarding] * self.dimension
            else:
                forwarding = self.domain_forwarding

            for n, (dl, d) in enumerate(zip(self.domain_labels, self.domain)):
                if forwarding[n]:
                    # find set names to grow (bottom to top)
                    to_grow = []
                    while isinstance(d, abcs.ABCSet):
                        to_grow.append(d.name)
                        d = d.domain[0]

                    # grow the sets (top to bottom)
                    to_grow.reverse()
                    for i in to_grow:
                        if self.container[i].records is not None:
                            recs = self.container[i].records

                            assert (
                                self.container[i].dimension == 1
                            ), "attempting to forward a domain set that has dimension >1"

                            # convert all categoricals back to str to enable concat
                            recs.isetitem(0, recs.iloc[:, 0].astype(str))

                            df = pd.DataFrame(self.records[dl])
                            df = df.assign(element_text="")
                            df.columns = recs.columns

                            recs = pd.concat([recs, df], ignore_index=True)

                            # clean up any non-unique set elements, should they exist
                            recs.drop_duplicates(
                                subset=recs.columns[0],
                                keep="first",
                                inplace=True,
                                ignore_index=True,
                            )

                            # convert object back to categorical
                            recs.isetitem(
                                0,
                                recs.iloc[:, 0].astype(
                                    CategoricalDtype(
                                        recs.iloc[:, 0].unique(), ordered=True
                                    )
                                ),
                            )
                        else:
                            recs = pd.DataFrame(self.records[dl].unique())
                            recs = recs.assign(element_text="")

                            # convert object back to unlinked categorical
                            recs.isetitem(
                                0,
                                recs.iloc[:, 0].astype(
                                    CategoricalDtype(
                                        recs.iloc[:, 0].unique(), ordered=True
                                    )
                                ),
                            )

                        # set records
                        self.container[i].records = recs
                        self.container[i].domain_labels = self.container[i].domain_names
                        self.container[i].modified = True

    def _assert_valid_records(self):
        if self.records is not None:
            # make sure and all domains have valid categories
            for i in range(self.dimension):
                if np.any(self.records.iloc[:, i].cat.codes.to_numpy() == -1):
                    raise Exception(
                        f"Categories are missing from the data in symbol `{self.name}` (dimension {i}) -- "
                        "has resulted in `NaN` domains labels. "
                        "Cannot write symbol until domain labels have been been restored."
                    )

    def _assert_is_valid(self):
        if self._requires_state_check:
            # check if symbol has a container
            if self.container is None:
                raise Exception(
                    "Symbol is not currently linked to a container, "
                    "must add it to a container in order to be valid"
                )

            # check domain symbols
            for i in self.domain:
                if isinstance(i, abcs.AnyContainerDomainSymbol):
                    # must have valid links
                    if hex(id(i)) not in [
                        hex(id(v)) for _, v in self.container.data.items()
                    ]:
                        raise Exception(
                            f"Symbol defined over domain symbol `{i.name}`, "
                            "however the object reference "
                            f"'{hex(id(i))}' is not in the Container anymore "
                            f"-- must reset domain for symbol '{self.name}'."
                        )

                    # must be valid symbols
                    if not i.isValid():
                        raise Exception(
                            f"Symbol defined over domain symbol `{i.name}`, "
                            "however this object is not a valid object in the Container"
                            " -- all domain objects must be valid."
                        )

                    # cannot use singleton sets as domain sets
                    if getattr(i, "is_singleton", False):
                        raise Exception(
                            "Singleton sets cannot be used as a symbol domain set. "
                            f"Symbol '{self.name}' currently uses singleton set '{i.name}' in its domain definition."
                        )

            # if records exist do some checks
            if self.records is not None:
                # check if records are a DataFrame
                if not isinstance(self.records, pd.DataFrame):
                    raise Exception("Symbol 'records' must be type pandas.DataFrame")

                # check if self.records has the correct number of columns and/or rows
                r, c = self.records.shape
                if not c == self.dimension + len(self._attributes):
                    raise ValueError(
                        "Symbol 'records' does not have the correct "
                        " number of columns (<symbol dimension> + 1)"
                    )

                if self.dimension == 0:
                    if r > 1:
                        raise ValueError(
                            "Symbol 'records' can only have 1 row because "
                            f"it has been defined to be a scalar (currently has {r} rows)"
                        )

                # check that all domain_labels are unique
                if len(self.domain_labels) != len(set(self.domain_labels)):
                    raise Exception(
                        "Domain columns do not have unique names. "
                        "Reset domain column names by setting the `<symbol>.domain_labels` property."
                    )

                # check that all value columns have the same name as _attributes
                if self.records.columns[self.dimension :].tolist() != self._attributes:
                    raise Exception(
                        f"Value columns in 'records' must be named and ordered as: {self._attributes}. "
                        f"Currently named: {self.records.columns[self.dimension:]}"
                    )

                # check if domain columns are categorical dtype
                for i in self.domain_labels:
                    if not isinstance(self.records[i].dtype, CategoricalDtype):
                        raise Exception(
                            f"Domain information in column `{i}` for "
                            " 'records' must be categorical type"
                        )

                # check if domain categories are all type str
                for i in self.domain_labels:
                    typ = infer_dtype(self.records[i].cat.categories)
                    if typ != "empty":
                        if typ != "string":
                            raise TypeError(
                                f"Domain column `{i}` in 'records' contains non-str "
                                "category, all domain categories must be type str."
                            )

                # check if set element_text columns are type str
                if isinstance(self, abcs.ABCSet):
                    typ = infer_dtype(self.records["element_text"])
                    if typ != "empty":
                        if typ != "string":
                            raise TypeError(
                                "Records 'element_text' column must contain only str type"
                            )

                # check if all data_columns are type float
                if isinstance(
                    self, (abcs.ABCParameter, abcs.ABCVariable, abcs.ABCEquation)
                ):
                    for i in self.records.columns[self.dimension :]:
                        if infer_dtype(self.records[i]) != "empty":
                            if not is_float_dtype(self.records[i]):
                                raise Exception(
                                    f"Data in column `{i}` for 'records' must be float type"
                                )

            # if no exceptions, then turn self._requires_state_check 'off'
            self._requires_state_check = False

    def getSparsity(self):
        if self.domain_type in {"relaxed", "none"}:
            return float("nan")
        elif self.domain_type == "regular":
            dense = 1
            for i in [n.number_records for n in self.domain]:
                dense *= i

            return 1 - self.number_records / dense
