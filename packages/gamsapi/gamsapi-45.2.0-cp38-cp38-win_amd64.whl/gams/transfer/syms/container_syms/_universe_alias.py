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
from gams.core import gdx
from gams.transfer._abcs import ABCUniverseAlias, ABCAlias, AnyContainerSymbol
from gams.transfer.syms._mixins import SAUAMixin, SAUAPVEMixin


class UniverseAlias(SAUAMixin, SAUAPVEMixin, ABCUniverseAlias):
    @classmethod
    def _from_gams(cls, container, name):
        # create new symbol object
        obj = UniverseAlias.__new__(cls)

        # set private properties directly
        obj._requires_state_check = False
        obj._container = container
        container._requires_state_check = True
        obj._name = name
        obj._modified = True

        # typing
        obj._gams_type = gdx.GMS_DT_ALIAS
        obj._gams_subtype = 0

        # add to container
        container.data.update({name: obj})

        return obj

    def __new__(cls, *args, **kwargs):
        if len(args) == 0:
            return object.__new__(UniverseAlias)

        try:
            symobj = args[0][args[1]]
        except:
            symobj = None

        if symobj is None:
            return object.__new__(UniverseAlias)
        else:
            if isinstance(symobj, ABCUniverseAlias):
                return symobj
            else:
                raise TypeError(
                    f"Cannot overwrite symbol `{symobj.name}` in container because it is not a UniverseAlias object)"
                )

    def __init__(self, container, name):
        self._requires_state_check = True
        self.container = container
        self.name = name
        self.modified = True
        self._gams_type = gdx.GMS_DT_ALIAS
        self._gams_subtype = 0
        container.data.update({name: self})

    def __delitem__(self):
        # TODO: add in some functionality that might relax the symbols down to a different domain
        #       This function would mimic the <Container>.removeSymbols() method -- is more pythonic
        del self.container.data[self.name]

    def __repr__(self):
        return f"<UniverseAlias `{self.name}` ({hex(id(self))})>"

    @property
    def is_singleton(self):
        return False

    def _assert_is_valid(self):
        if self._requires_state_check:
            if self.container is None:
                raise Exception(
                    "Symbol is not currently linked to a container, "
                    "must add it to a container in order to be valid"
                )

            # if no exceptions, then turn self._requires_state_check 'off'
            self._requires_state_check = False

    @property
    def alias_with(self):
        return "*"

    @property
    def domain_names(self):
        return ["*"]

    @property
    def domain_labels(self):
        return ["uni"]

    @property
    def domain(self):
        return ["*"]

    @property
    def description(self):
        return "Aliased with *"

    @property
    def dimension(self):
        return 1

    def toList(self):
        if self.records is not None:
            return self.records.set_index(self.records.columns[0]).index.to_list()

    @property
    def records(self):
        if self.isValid():
            return pd.DataFrame(
                data=self.container.getUELs(), columns=self.domain_labels
            )

    @property
    def number_records(self):
        if self.isValid():
            return len(self.records)

        return float("nan")

    @property
    def domain_type(self):
        return "none"

    def getUELs(self, ignore_unused=False):
        if self.isValid():
            return self.container.getUELs(ignore_unused=ignore_unused)

    @property
    def summary(self):
        return {
            "name": self.name,
            "description": self.description,
            "alias_with": self.alias_with,
        }

    def equals(
        self,
        other,
        check_meta_data=True,
        verbose=False,
    ):
        try:
            #
            # ARG: other
            if not isinstance(other, AnyContainerSymbol):
                raise TypeError(
                    "Argument 'other' must be a GAMS Container Symbol object"
                )

            # adjustments
            if isinstance(other, ABCAlias):
                other = other.alias_with

            #
            # ARG: self & other
            if not isinstance(self, type(other)):
                raise TypeError(
                    f"Symbol are not of the same type (`{type(self)}` != `{type(other)}`)"
                )

            #
            # ARG: check_meta_data
            if not isinstance(check_meta_data, bool):
                raise TypeError("Argument 'check_meta_data' must be type bool")

            #
            # Mandatory checks
            if not self.isValid():
                raise Exception(
                    f"Cannot compare objects because `{self.name}` is not a valid symbol object"
                    "Use `<symbol>.isValid(verbose=True)` to debug further."
                )

            if not other.isValid():
                raise Exception(
                    f"Cannot compare objects because `{other.name}` is not a valid symbol object"
                    "Use `<symbol>.isValid(verbose=True)` to debug further."
                )

            #
            # Check metadata (optional)
            if check_meta_data:
                if self.name != other.name:
                    raise Exception(
                        f"Symbol names do not match (`{self.name}` != `{other.name}`)"
                    )

            return True
        except Exception as err:
            if verbose:
                raise err
            else:
                return False

    def pivot(self, *args, **kwargs):
        raise Exception(
            "Pivoting operations only possible on symbols with dimension > 1, "
            f"symbol dimension is {self.dimension}"
        )

    def getSparsity(self):
        return 0.0
