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

from gams import transfer as gt
import pandas as pd
from gams.core.embedded import ECGAMSDatabase
from gams.core.gmd import *
from gams.connect.agents.connectagent import ConnectAgent

class GAMSWriter(ConnectAgent):

    def __init__(self, system_directory, cdb, inst):
        super().__init__(system_directory, cdb, inst)
        self._symbols = inst.get("symbols", [])
        self._write_all = inst.get("writeAll", "auto")
        if self._write_all == "auto":
            self._write_all = True if self._symbols == [] else False
        self._duplicateRecords = inst.get("duplicateRecords", "all")
        self._trace = inst.get("trace", cdb.options.get('trace',0))
        if self._trace > 3:
            pd.set_option("display.max_rows", None, "display.max_columns", None)
        if not (self._cdb.ecdb and isinstance(self._cdb.ecdb, ECGAMSDatabase)):
           self.connect_error(f"GAMSWriter is running without GAMS context.")
        elif self._cdb.ecdb.arguments.startswith('@connectOut'): # we run with GAMS cmd parameter connectOut
           self.connect_error(f"GAMSWriter not available for connectOut scripts.")

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
            self._cdb._container.write(self._cdb.ecdb.db._gmd, eps_to_zero=False)
            gmd_list = self._cdb._container.listSymbols()
        else:
            sym_names = [ ]
            # Since we can't copy invalid symbols (=symbols with duplicates) we need to resolve the duplicates in the Connect container
            for sym in self._symbols:
                dr = sym.get("duplicateRecords", self._duplicateRecords)
                if dr != "all":
                    self._cdb._container.data[sym['name']].dropDuplicateRecords(keep=drmap[dr])
                sym_names.append(sym['name'])
            gms = gt.Container(system_directory=self._system_directory)
            gms.read(self._cdb._container, sym_names)

            # Apply original categories of * domains in new Container
            for sym_name in gms.listSymbols():
                ssym = self._cdb._container.data[sym_name]
                tsym = gms.data[sym_name]
                if ssym.records is None:
                    continue
                for d, tdl, sdl in zip(tsym.domain, tsym.domain_labels, ssym.domain_labels):
                    if type(d) == str:
                        tsym.records[tdl] = tsym.records[tdl].astype(pd.CategoricalDtype(categories=ssym.records[sdl].cat.categories, ordered=True))

            # Renaming
            if self._trace > 0:
                self._cdb.print_log(f'GAMS symbols: {gms.listSymbols()}\n')
            sym_map = {}
            for sym in self._symbols:
                if 'newName' in sym:
                    gms.renameSymbol(sym['name'], sym['newName'])
                    sym_map[sym['newName']] = sym
                else:
                    sym_map[sym['name']] = sym

            if self._trace > 0:
                self.describe_container(gms, 'GAMS Container')
            if self._trace > 2:
                for name, sym in gms.data.items():
                    self._cdb.print_log(f'GAMS Container symbol={name}:\n {sym.records}\n')
            gms.write(self._cdb.ecdb.db._gmd, eps_to_zero=False)
            gmd_list = gms.listSymbols()

        # Build the modSymList with merge type and domain check type
        merge_type_lookup = {'replace':0, 'merge':1, 'default':2}
        domain_check_type_lookup = {'filtered':0, 'checked':1, 'default':2}
        global_mt = merge_type_lookup.get(self._inst.get("mergeType", "default"), 2)
        global_dct = domain_check_type_lookup.get(self._inst.get("domainCheckType", "default"), 2)
        rc = new_intp()
        self._cdb.ecdb._modSymList = {}
        for sym_name in gmd_list:
            sym_ptr = gmdFindSymbolPy(self._cdb.ecdb.db._gmd, sym_name, rc)
            if not intp_value(rc):
                self.connect_error(gmdGetLastError(self._cdb.ecdb.db._gmd)[1])
            ret = gmdSymbolInfo(self._cdb.ecdb.db._gmd, sym_ptr, GMD_NUMBER)
            if not ret[0]:
                self.connect_error(gmdGetLastError(self._cdb.ecdb.db._gmd)[1])
            if self._write_all:
                self._cdb.ecdb._modSymList[ret[1]] = (global_mt, global_dct)
            else:
                sym = sym_map[sym_name]
                mt = merge_type_lookup[sym["mergeType"]] if "mergeType" in sym else global_mt
                dct = domain_check_type_lookup[sym["domainCheckType"]] if "domainCheckType" in sym else global_dct
                self._cdb.ecdb._modSymList[ret[1]] = (mt, dct)
        delete_intp(rc)
