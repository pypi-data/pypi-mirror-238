#****************************************************************************
#* core_lib_factory.py
#*
#* Copyright 2022 Matthew Ballance and Contributors
#*
#* Licensed under the Apache License, Version 2.0 (the "License"); you may 
#* not use this file except in compliance with the License.  
#* You may obtain a copy of the License at:
#*
#*   http://www.apache.org/licenses/LICENSE-2.0
#*
#* Unless required by applicable law or agreed to in writing, software 
#* distributed under the License is distributed on an "AS IS" BASIS, 
#* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  
#* See the License for the specific language governing permissions and 
#* limitations under the License.
#*
#* Created on:
#*     Author: 
#*
#****************************************************************************
from ..context import Context
from ..context import DataTypeFunctionFlags

class CoreLibFactory(object):

    def __init__(self, ctxt):
        self._ctxt = ctxt
        pass

    def build(self):
        self._buildRegFuncs()
        self._buildRegGroupFuncs()
        self._buildIO()
        pass

    def _buildIO(self):
        print_f = self._ctxt.mkDataTypeFunction(
            "std_pkg::print",
            None,
            False,
            DataTypeFunctionFlags.Core)
        print("Add std_pkg::print to library")
        self._ctxt.addDataTypeFunction(print_f)
        print_f.addImportSpec(
            self._ctxt.mkDataTypeFunctionImport("X", False, False))

    def _buildRegGroupFuncs(self):
        set_handle = self._ctxt.mkDataTypeFunction(
            "pss::core::reg_group::set_handle",
            None,
            False,
            DataTypeFunctionFlags.Core)
        self._ctxt.addDataTypeFunction(set_handle)
        set_handle.addImportSpec(
            self._ctxt.mkDataTypeFunctionImport("X", False, False))

    def _buildRegFuncs(self):
        reg_read = self._ctxt.mkDataTypeFunction(
            "pss::core::reg_read",
            self._ctxt.findDataTypeInt(False, 64),
            False,
            DataTypeFunctionFlags.Core)
        reg_read.addImportSpec(
            self._ctxt.mkDataTypeFunctionImport("X", False, False))
        self._ctxt.addDataTypeFunction(reg_read)
        reg_read_val = self._ctxt.mkDataTypeFunction(
            "pss::core::reg_read_val",
            self._ctxt.findDataTypeInt(False, 64),
            False,
            DataTypeFunctionFlags.Core)
        reg_read_val.addImportSpec(
            self._ctxt.mkDataTypeFunctionImport("X", False, False))
        self._ctxt.addDataTypeFunction(reg_read_val)
        reg_write = self._ctxt.mkDataTypeFunction(
            "pss::core::reg_write",
            None,
            False,
            DataTypeFunctionFlags.Core)
        reg_write.addImportSpec(
            self._ctxt.mkDataTypeFunctionImport("X", False, False))
        self._ctxt.addDataTypeFunction(reg_write)
        reg_write_val = self._ctxt.mkDataTypeFunction(
            "pss::core::reg_write_val",
            None,
            False,
            DataTypeFunctionFlags.Core)
        reg_write_val.addImportSpec(
            self._ctxt.mkDataTypeFunctionImport("X", False, False))
        self._ctxt.addDataTypeFunction(reg_write_val)

