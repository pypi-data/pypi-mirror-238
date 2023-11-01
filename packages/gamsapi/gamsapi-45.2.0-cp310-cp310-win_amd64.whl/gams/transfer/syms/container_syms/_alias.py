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

from gams.core import gdx
from gams.transfer._abcs import ABCSet, ABCAlias, ABCUniverseAlias, ABCContainer
from gams.transfer.syms._mixins import SAMixin, SAPVEMixin, SAUAMixin, SAUAPVEMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gams.transfer import Container
    from gams.transfer import Set


class Alias(SAMixin, SAPVEMixin, SAUAMixin, SAUAPVEMixin, ABCAlias):
    @classmethod
    def _from_gams(cls, container, name, alias_with):
        # create new symbol object
        obj = Alias.__new__(cls)

        # set private properties directly
        obj._requires_state_check = False
        obj._container = container
        container._requires_state_check = True
        obj._name = name
        obj._alias_with = alias_with
        obj._modified = True

        # typing
        obj._gams_type = gdx.GMS_DT_ALIAS
        obj._gams_subtype = 1

        # add to container
        container.data.update({name: obj})

        return obj

    def __new__(cls, *args, **kwargs):
        if len(args) == 0:
            return object.__new__(Alias)

        try:
            symobj = args[0][args[1]]
        except:
            symobj = None

        if symobj is None:
            return object.__new__(Alias)
        else:
            if isinstance(symobj, ABCAlias):
                return symobj
            else:
                raise TypeError(
                    f"Cannot overwrite symbol `{symobj.name}` in container because it is not an Alias object)"
                )

    def __init__(self, container: "Container", name: str, alias_with: "Set"):
        """Alias of a Set

        Parameters
        ----------
        container : Container
        name : str
        alias_with : Set

        Example
        ----------
        >>> m = gt.Container()
        >>> i = gt.Set(m, "i")
        >>> j = gt.Alias(m, "j", i)
        """

        # does symbol exist
        has_symbol = False
        if isinstance(getattr(self, "container", None), ABCContainer):
            has_symbol = True

        if has_symbol:
            # reset some properties
            self._requires_state_check = True
            self.container._requires_state_check = True
            self.modified = True
            self.alias_with = alias_with

        else:
            # populate new symbol properties
            self._requires_state_check = True
            self.container = container
            self.name = name
            self.modified = True
            self.alias_with = alias_with
            self._gams_type = gdx.GMS_DT_ALIAS
            self._gams_subtype = 1
            container.data.update({name: self})

    def __repr__(self):
        return f"<Alias `{self.name}` ({hex(id(self))})>"

    def __delitem__(self):
        # TODO: add in some functionality that might relax the symbols down to a different domain
        #       This function would mimic the <Container>.removeSymbols() method -- is more pythonic
        del self.container.data[self.name]

    def equals(
        self,
        other,
        check_uels=True,
        check_element_text=True,
        check_meta_data=True,
        verbose=False,
    ):
        return self.alias_with.equals(
            other,
            check_uels=check_uels,
            check_element_text=check_element_text,
            check_meta_data=check_meta_data,
            verbose=verbose,
        )

    def toList(self, include_element_text=False):
        return self.alias_with.toList(include_element_text=include_element_text)

    def pivot(self, index=None, columns=None, fill_value=None):
        return self.alias_with.pivot(
            index=index, columns=columns, fill_value=fill_value
        )

    def getSparsity(self):
        return self.alias_with.getSparsity()

    @property
    def is_singleton(self):
        return self.alias_with.is_singleton

    @is_singleton.setter
    def is_singleton(self, is_singleton):
        self.alias_with.is_singleton = is_singleton
        self.modified = True

    def getDomainViolations(self):
        return self.alias_with.getDomainViolations()

    def findDomainViolations(self):
        return self.alias_with.findDomainViolations()

    def hasDomainViolations(self):
        return self.alias_with.hasDomainViolations()

    def countDomainViolations(self):
        return self.alias_with.countDomainViolations()

    def dropDomainViolations(self):
        return self.alias_with.dropDomainViolations()

    def countDuplicateRecords(self):
        return self.alias_with.countDuplicateRecords()

    def findDuplicateRecords(self, keep="first"):
        return self.alias_with.findDuplicateRecords(keep=keep)

    def hasDuplicateRecords(self):
        return self.alias_with.hasDuplicateRecords()

    def dropDuplicateRecords(self, keep="first"):
        return self.alias_with.dropDuplicateRecords(keep=keep)

    def _getUELCodes(self, dimension, ignore_unused=False):
        return self.alias_with._getUELCodes(dimension, ignore_unused=ignore_unused)

    def getUELs(self, dimensions=None, codes=None, ignore_unused=False):
        return self.alias_with.getUELs(
            dimensions=dimensions, codes=codes, ignore_unused=ignore_unused
        )

    def lowerUELs(self, dimensions=None):
        self.alias_with.lowerUELs(dimensions=dimensions)
        return self

    def upperUELs(self, dimensions=None):
        self.alias_with.upperUELs(dimensions=dimensions)
        return self

    def lstripUELs(self, dimensions=None):
        self.alias_with.lstripUELs(dimensions=dimensions)
        return self

    def rstripUELs(self, dimensions=None):
        self.alias_with.rstripUELs(dimensions=dimensions)
        return self

    def stripUELs(self, dimensions=None):
        self.alias_with.stripUELs(dimensions=dimensions)
        return self

    def capitalizeUELs(self, dimensions=None):
        self.alias_with.capitalizeUELs(dimensions=dimensions)
        return self

    def casefoldUELs(self, dimensions=None):
        self.alias_with.casefoldUELs(dimensions=dimensions)
        return self

    def titleUELs(self, dimensions=None):
        self.alias_with.titleUELs(dimensions=dimensions)
        return self

    def ljustUELs(self, length, fill_character=None, dimensions=None):
        self.alias_with.ljustUELs(
            length, fill_character=fill_character, dimensions=dimensions
        )
        return self

    def rjustUELs(self, length, fill_character=None, dimensions=None):
        self.alias_with.rjustUELs(
            length, fill_character=fill_character, dimensions=dimensions
        )
        return self

    def setUELs(self, uels, dimensions=None, rename=False):
        return self.alias_with.setUELs(uels=uels, dimensions=dimensions, rename=rename)

    def reorderUELs(self, uels=None, dimensions=None):
        return self.alias_with.reorderUELs(uels=uels, dimensions=dimensions)

    def addUELs(self, uels, dimensions=None):
        return self.alias_with.addUELs(uels=uels, dimensions=dimensions)

    def removeUELs(self, uels=None, dimensions=None):
        return self.alias_with.removeUELs(uels=uels, dimensions=dimensions)

    def renameUELs(self, uels, dimensions=None, allow_merge=False):
        return self.alias_with.renameUELs(
            uels=uels, dimensions=dimensions, allow_merge=allow_merge
        )

    def _assert_valid_records(self):
        self.alias_with._assert_valid_records()

    def _assert_is_valid(self):
        if self._requires_state_check:
            if self.container is None:
                raise Exception(
                    "Symbol is not currently linked to a container, "
                    "must add it to a container in order to be valid"
                )

            if self.alias_with is None:
                raise Exception(
                    "Alias symbol is not valid because it is not currently linked to a parent set"
                )

            if not self.alias_with.isValid():
                raise Exception(
                    "Alias symbol is not valid because parent "
                    f"set '{self.alias_with.name}' is not valid"
                )
            # if no exceptions, then turn self._requires_state_check 'off'
            self._requires_state_check = False

    @property
    def alias_with(self):
        return self._alias_with

    @alias_with.setter
    def alias_with(self, alias_with):
        if isinstance(alias_with, ABCUniverseAlias):
            raise TypeError(
                "Cannot create an Alias to a UniverseAlias, create a new UniverseAlias symbol instead."
            )

        if not isinstance(alias_with, (ABCSet, ABCAlias)):
            raise TypeError("Symbol 'alias_with' must be type Set or Alias")

        if isinstance(alias_with, ABCAlias):
            parent = alias_with
            while not isinstance(parent, ABCSet):
                parent = parent.alias_with
            alias_with = parent

        # check to see if _alias_with is being changed
        if getattr(self, "_alias_with", None) != alias_with:
            self._requires_state_check = True
            self._alias_with = alias_with
            self.modified = True

            if isinstance(self.container, ABCContainer):
                self.container._requires_state_check = True
                self.container.modified = True

    @property
    def domain_names(self):
        return self.alias_with.domain_names

    @property
    def domain(self):
        return self.alias_with.domain

    @domain.setter
    def domain(self, domain):
        self.alias_with.domain = domain
        self.modified = True
        self.container.modified = True

    @property
    def domain_type(self):
        return self.alias_with.domain_type

    @property
    def description(self):
        return self.alias_with.description

    @description.setter
    def description(self, description):
        self.alias_with.description = description
        self.modified = True
        self.container.modified = True

    @property
    def dimension(self):
        return self.alias_with.dimension

    @dimension.setter
    def dimension(self, dimension):
        self.alias_with.dimension = dimension
        self.modified = True
        self.container.modified = True

    @property
    def records(self):
        return self.alias_with.records

    @records.setter
    def records(self, records):
        self.alias_with.records = records
        self.modified = True
        self.container.modified = True

    def setRecords(self, records, uels_on_axes=False):
        self.alias_with.setRecords(records, uels_on_axes=uels_on_axes)

    @property
    def number_records(self):
        return self.alias_with.number_records

    @property
    def domain_labels(self):
        return self.alias_with.domain_labels

    @domain_labels.setter
    def domain_labels(self, labels):
        self.alias_with.domain_labels = labels

    @property
    def summary(self):
        return {
            "name": self.name,
            "description": self.description,
            "alias_with": self.alias_with.name,
            "is_singleton": self.is_singleton,
            "domain": self.domain_names,
            "domain_type": self.domain_type,
            "dimension": self.dimension,
            "number_records": self.number_records,
        }
