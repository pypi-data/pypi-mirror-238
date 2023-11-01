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
from gams import transfer as gt
import pandas as pd
from gams.connect.agents.connectagent import ConnectAgent

class GDXWriter(ConnectAgent):

    def __init__(self, system_directory, cdb, inst):
        super().__init__(system_directory, cdb, inst)
        self._symbols = inst.get("symbols", [])
        self._write_all = inst.get("writeAll", "auto")
        if self._write_all == "auto":
            self._write_all = True if self._symbols == [] else False
        self._duplicateRecords = inst.get("duplicateRecords", "all")
        self._gdx_file = os.path.abspath(inst["file"])
        self._trace = inst.get("trace", cdb.options.get('trace',0))
        if self._trace > 3:
            pd.set_option("display.max_rows", None, "display.max_columns", None)

    def execute(self):
        drmap = {'none': False, 'first': 'first', 'last': 'last'}
        if self._write_all:
            if self._trace > 0:
                self.describe_container(self._cdb._container, 'Connect Container')
            if self._trace > 2:
                for name, sym in self._cdb._container.data.items():
                    self._cdb.print_log(f'Connect Container symbol={name}:\n {sym.records}\n')
            if self._duplicateRecords != "all":
                self._cdb._container.dropDuplicateRecords(keep=drmap[self._duplicateRecords])
            self._cdb._container.write(self._gdx_file, eps_to_zero=False)
        else:
            sym_names = [ ]
            # Since we can't copy invalid symbols (=symbols with duplicates) we need to resolve the duplicates in the Connect container
            for sym in self._symbols:
                dr = sym.get("duplicateRecords", self._duplicateRecords)
                if dr != "all":
                    self._cdb._container.data[sym['name']].dropDuplicateRecords(keep=drmap[dr])
                sym_names.append(sym['name'])
            gdx = gt.Container(system_directory=self._system_directory)
            gdx.read(self._cdb._container, sym_names)

            # Apply original categories of * domains in new Container
            for sym_name in gdx.listSymbols():
                ssym = self._cdb._container.data[sym_name]
                tsym = gdx.data[sym_name]
                if ssym.records is None:
                    continue
                for d, tdl, sdl in zip(tsym.domain, tsym.domain_labels, ssym.domain_labels):
                    if type(d) == str:
                        tsym.records[tdl] = tsym.records[tdl].astype(pd.CategoricalDtype(categories=ssym.records[sdl].cat.categories, ordered=True))

            # Renaming
            if self._trace > 0:
                self._cdb.print_log(f'GDX symbols: {gdx.listSymbols()}\n')
            for sym in self._symbols:
                if 'newName' in sym:
                    gdx.renameSymbol(sym['name'], sym['newName'])

            if self._trace > 0:
                self.describe_container(gdx, 'GDX Container')
            if self._trace > 2:
                for name, sym in gdx.data.items():
                    self._cdb.print_log(f'GDX Container symbol={name}:\n {sym.records}\n')
                    self._cdb.print_log(f'  Valid: {sym.isValid(verbose=True)}\n');
            gdx.write(self._gdx_file, eps_to_zero=False)
