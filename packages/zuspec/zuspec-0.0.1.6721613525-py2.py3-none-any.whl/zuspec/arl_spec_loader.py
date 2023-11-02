#****************************************************************************
#* arl_spec_loader.py
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

import zuspec
import zsp_arl_dm.core as arl_dm
import zsp_fe_parser.core as zsp_fe_parser
import sys
import importlib
from typing import List
import zsp_parser.core as zspp

class ArlSpecLoader(object):
    """Loads an ARL specification from a mix of inputs"""

    def __init__(self, ctxt=None):
        self._spec_segments = []
        if ctxt is None:
            self._ctxt = zuspec.Zuspec.context;
        else:
            self._ctxt = ctxt
        self._pythonpath = []
        pass

    @property
    def ctxt(self):
        return self._ctxt

    def addLoadPyModule(self, module):
        spec = ArlSpecLoader.LoadSegmentPython(self, module)
        self._spec_segments.append(spec)

    def addPythonPath(self, path):
        self._pythonpath.append(path)

    def addLoadPss(self, files : List[str]):
        spec = ArlSpecLoader.LoadSegmentPss(self, files)
        self._spec_segments.append(spec)

    def load(self):
        import zsp_dataclasses

        for s in self._spec_segments:
            s.load()

        zsp_dataclasses.impl.Ctor.inst().elab()

    class LoadSegmentPython(object):

        def __init__(self, loader, module):
            self.loader = loader
            self.module = module
            pass

        def load(self):
            from vsc_dataclasses.impl import Ctor 
            orig_path = sys.path.copy()
            orig_ps = Ctor.inst().setTypePS("::")
            try:
                if len(self.loader._pythonpath) > 0:
                    for e in self.loader._pythonpath:
                        sys.path.insert(0, e)

                print("sys.path=%s" % str(sys.path))
                m = importlib.import_module(self.module)
                print("Module: %s" % str(m))
            finally:
                sys.path = orig_path
                Ctor.inst().setTypePS(orig_ps)

            # TODO: after load, need to elaborate any elements that were loaded

            pass

    class LoadSegmentPss(object):

        def __init__(self, loader, files):
            self.loader = loader
            self.files = files.copy()

        def load(self):
            zspp_f = zspp.Factory.inst()
            ast_f = zspp_f.getAstFactory()
            marker_c = zspp_f.mkMarkerCollector()

            ast_builder = zspp_f.mkAstBuilder(marker_c)
            ast_linker = zspp_f.mkAstLinker()

            scopes = []

            scope = ast_f.mkGlobalScope(len(scopes))
            zspp_f.loadStandardLibrary(ast_builder, scope)
            scopes.append(scope)

            for file in self.files:
                scope = ast_f.mkGlobalScope(len(scopes))

                with open(file, "r") as fp:
                    ast_builder.build(scope, fp)

                scopes.append(scope)

                if marker_c.hasSeverity(zspp.MarkerSeverityE.Error):
                    break

            if marker_c.hasSeverity(zspp.MarkerSeverityE.Error):
                raise Exception("Syntax error")
                return

            link_root = ast_linker.link(marker_c, scopes)

            if marker_c.hasSeverity(zspp.MarkerSeverityE.Error):
                raise Exception("Link error")
                return

            zsp_arl_f = arl_dm.Factory.inst()
            ast2arl_ctxt = zsp_fe_parser.Factory.inst().mkAst2ArlContext(
                self.loader._ctxt,
                marker_c)

            ast2arl_builder = zsp_fe_parser.Factory.inst().mkAst2ArlBuilder()
            ast2arl_builder.build(link_root, ast2arl_ctxt)
            pass




