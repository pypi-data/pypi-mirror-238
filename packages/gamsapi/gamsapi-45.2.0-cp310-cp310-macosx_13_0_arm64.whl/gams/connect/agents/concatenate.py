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

import gams.transfer as gt
import pandas as pd
from gams.connect.agents.connectagent import ConnectAgent
import re
import numpy as np

class Concatenate(ConnectAgent):

    def __init__(self, system_directory, cdb, inst):
        super().__init__(system_directory, cdb, inst)
        self.__gt2pytypemap__ = {gt.Set: 'set', gt.Parameter: 'parameter'}

        # global options
        self._output_dimensions = inst.get("outputDimensions", "all")
        self._dimension_map = inst.get("dimensionMap", {})
        self._universal_dimension = inst.get("universalDimension", "uni")
        self._emptyuel = inst.get("emptyUel", "-")
        self._output_name = {}
        self._output_name['set'] = inst.get("setName", "setOutput")
        self._output_name['parameter'] = inst.get("parameterName", "parameterOutput")
        self._concatenate_all = inst.get("concatenateAll", "auto")
        self._trace = inst.get("trace", cdb.options.get('trace', 0))
        if self._trace > 3:
            pd.set_option("display.max_rows", None, "display.max_columns", None)

        # symbol options
        self._symbols = inst.get("symbols", [])

    def execute(self):
        if self._trace > 0:
            self.describe_container(self._cdb._container, 'Connect Container')

        if self._concatenate_all == "auto":
            self._concatenate_all = not self._symbols

        if self._concatenate_all:
            self._symbols = []
            for name, sym in self._cdb._container.data.items():
                if type(sym) in [gt.Set, gt.Parameter]:
                    self._symbols.append({'name': name})

        remove_symbols = []  # remove symbols with no data
        count_symbols = {}
        for i, sym_opt in enumerate(self._symbols):
            regex = r'(?P<name>[a-zA-Z0-9_]+)?(\((?P<domains>[a-zA-Z0-9_,]+)\))?'
            ms = re.fullmatch(regex, sym_opt['name'])
            assert ms, f"Invalid symbol name {sym_opt['name']}."
            sym_opt['sname'] = ms.group('name')
            sym_no_case = sym_opt['sname'].casefold()
            count_symbols[sym_no_case] = count_symbols.get(sym_no_case, 0) + 1
            sym = self._cdb._container.data[sym_opt['sname']]

            if sym.records is None:
                remove_symbols.append(i)
                continue

            if type(sym) not in [gt.Set, gt.Parameter]:
                self.connect_error(f"Symbol type >{type(sym)}< of symbol >{sym_opt['sname']}< is not supported. Supported symbol types are sets and parameters. If you would like to concatenate variables or equations, use Connect Agent Projection to turn these into parameters.")
            if self._trace > 2:
                self._cdb.print_log(f"Connect Container symbol={sym_opt['sname']}:\n {sym.records}\n")

            if ms.group('domains'):
                sym_opt['dim'] = ms.group('domains').split(',')
                if sym.dimension != len(sym_opt['dim']):
                    self.connect_error(f"Number of specified dimensions of symbol >{sym_opt['name']}< does not correspond to the symbol's number of dimensions in the database ({len(sym_opt['dim'])}<>{sym.dimension}).")
            else:
                sym_opt['dim'] = []
                if sym.dimension > 0:  # if symbol dim is not specified: use dimension_map to map domains to output dimensions, domains that cannot be mapped will be universal output dimensions
                    sym_opt['dim'] = [self._dimension_map.get(d, d) for d in sym.domain_names]

        for i in reversed(remove_symbols):
            del self._symbols[i]

        if not self._symbols:
            self._cdb.print_log(f"No data to concatenate.")
            return

        # if outputDimensions is all, generate output dimensions from symbol dimensions
        if self._output_dimensions == "all":
            self._output_dimensions = []
            for sym_opt in self._symbols:
                for idx, d in enumerate(sym_opt['dim']):
                    if d not in self._output_dimensions:
                        self._output_dimensions.append(d)
                    elif self._output_dimensions.count(d) < sym_opt['dim'][:idx + 1].count(d):
                        self._output_dimensions.append(d)
        else:
            regex = r'([a-zA-Z0-9_]+)'
            invalid_dim = [dim for dim in self._output_dimensions if not re.fullmatch(regex, dim)]
            if invalid_dim != []:
                self.connect_error(f"Invalid output dimension(s) >{invalid_dim}<.")

        if "symbols" in self._output_dimensions:
            self.connect_error("'symbols' is a preserved output dimension.")

        # collect dataframes to concatenate
        output_types = set()
        added_uni_columns = 0
        dataframes = {'set': [], 'parameter': []}
        original_sym_columns = {}
        GT_NA_values = []

        def make_dimensions_unique(dim_list):
            cp_dim_list = dim_list.copy()
            counts={}
            for i, dim in enumerate(cp_dim_list):
                cur_count = counts.get(dim, 0)
                if cur_count > 0:
                    cp_dim_list[i] = '%s.%d' % (dim, cur_count)
                counts[dim] = cur_count + 1
            return cp_dim_list

        # make output dimensions unique, e.g. ['i', 'j', 'j'] -> ['i', 'j', 'j.1']
        unique_output_dimensions = make_dimensions_unique(self._output_dimensions)

        for sym_opt in self._symbols:
            sym = self._cdb._container.data[sym_opt['sname']]
            output_types.add(self.__gt2pytypemap__[type(sym)])

            if sym.dimension > 0:
                # make symbol dimensions unique
                sym_opt['dim'] = make_dimensions_unique(sym_opt['dim'])

                # identify unknown dimensions, unknown dimensions will be aggregated into universal output dimensions
                unknown_dim = [i for i, x in enumerate(sym_opt['dim']) if x not in unique_output_dimensions]

                if added_uni_columns < len(unknown_dim):  # add universal columns
                    for i in range(added_uni_columns, len(unknown_dim)):
                        uni_name = f'{self._universal_dimension}_{i}'
                        if uni_name in self._output_dimensions:
                            self.connect_error(f"Automatically added universal column >{uni_name}< is already specified under option outputDimensions. Please set another base name for universal dimensions via option universalDimension or rename the output dimension.")
                        unique_output_dimensions.append(uni_name)
                        self._output_dimensions.append(uni_name)
                        added_uni_columns += 1
                
                used_uni_columns = 0
                for i in unknown_dim:  # overwrite current dim name with universal column name
                    sym_opt['dim'][i] = f'{self._universal_dimension}_{used_uni_columns}'
                    used_uni_columns += 1

                if self._trace > 1:
                    self._cdb.print_log(f"Dimension(s) of symbol={sym_opt['name']}:\n {sym_opt['dim']}\n")

            # save original column names and rename columns (to avoid making a copy of the dataframes)
            # if a symbol is concatenated more than once we need to make a copy
            sym_no_case = sym_opt['sname'].casefold()
            if count_symbols[sym_no_case] > 1:
                sym_records = sym.records.copy()
                sym_opt['records_copy'] = True
                count_symbols[sym_no_case] -= 1
            else: 
                sym_records = sym.records
                original_sym_columns[sym_opt['sname']] = sym_records.columns.copy()
            val_col = "text" if type(sym) == gt.Set else "value"
            sym_records.columns = sym_opt['dim']+[val_col]
            # insert symbols column
            new_name = sym_opt.get('newName', sym_opt['sname'])
            sym_records.insert(loc=0, column='symbols', value=new_name)
            dataframes[self.__gt2pytypemap__[type(sym)]].append(sym_records)

            if isinstance(sym, gt.Parameter):
                if all(sym_records[val_col].isna()): # recover only if all records are NAs according to pandas
                    GT_NA_values.extend(gt.SpecialValues.isNA(sym_records[val_col]))
                else:
                    GT_NA_values.extend([False]*len(sym_records[val_col]))

        outputs = {}
        output_types = sorted(output_types, reverse=True)
        for ot in output_types:
            val_col = "text" if ot == "set" else "value"
            outputs[ot] = pd.concat([pd.DataFrame([], columns=['symbols']+unique_output_dimensions+[val_col])]+dataframes[ot])

            if ot == "parameter" and any(GT_NA_values): # recover gt.SpecialValues.NA
                outputs[ot] = outputs[ot].astype({"value": np.dtype("object")}) # needs to be data type object for mask to work with gt.SpecialValues.NA
                outputs[ot]["value"].mask(GT_NA_values, gt.SpecialValues.NA, inplace=True)
                #outputs[ot].loc[GT_NA_values, "value"] = gt.SpecialValues.NA # works in general but not with gt.SpecialValues.NA

            df = outputs[ot]
            for c in df[df.columns[1:-1]]:
                if pd.api.types.is_categorical_dtype(df[c]):
                    df[c] = df[c].cat.add_categories(self._emptyuel)

            outputs[ot].reset_index(inplace=True, drop=True)
            outputs[ot][outputs[ot].columns[1:-1]] = outputs[ot][outputs[ot].columns[1:-1]].fillna(self._emptyuel)

        # restore symbols
        for sym_opt in self._symbols:
            if 'records_copy' not in sym_opt.keys():
                sym = self._cdb._container.data[sym_opt['sname']]
                sym.records.drop(columns="symbols", inplace=True)
                sym.records.columns = original_sym_columns[sym_opt['sname']]

        # write outputs to database
        for ot in output_types:
            if ot == 'set':
                self._cdb._container.addSet(self._output_name[ot], domain=['symbols']+self._output_dimensions, records=outputs[ot])
            elif ot == 'parameter':
                self._cdb._container.addParameter(self._output_name[ot], domain=['symbols']+self._output_dimensions, records=outputs[ot])

            if self._trace > 2:
                self._cdb.print_log(f"Connect Container symbol={self._output_name[ot]}:\n {self._cdb._container.data[self._output_name[ot]].records}\n")

        if self._trace > 0:
            self.describe_container(self._cdb._container, 'Connect Container')
