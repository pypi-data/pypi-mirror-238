#****************************************************************************
#* loader.py
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
import io
import os
import zsp_arl_dm.core as arl_dm
import zsp_fe_parser.core as zsp_fe_parser
import zsp_parser.core as zspp

class Loader(object):

    def __init__(self, ctxt=None):
        if ctxt is None:
            self.ctxt = arl_dm.Factory.inst().mkContext()
        else:
            self.ctxt = ctxt
        self._zspp_f = zspp.Factory.inst()
        self._ast_f = self._zspp_f.getAstFactory()
        pass

    def load(self, *args, **kwargs):

        marker_c = self._zspp_f.mkMarkerCollector()

        ast_builder = self._zspp_f.mkAstBuilder(marker_c)

        roots = []

        # First, load up the core package
        scope = self._ast_f.mkGlobalScope(len(roots));
        self._zspp_f.loadStandardLibrary(
            ast_builder,
            scope)
        roots.append(scope)

        if marker_c.hasSeverity(zspp.MarkerSeverityE.Error):
            raise Exception("Failed to load core library")
        
        for i,in_s in enumerate(args):
            s = None
            name = None
            if hasattr(in_s, "read"):
                # Stream-line object
                s = in_s
            elif type(in_s) is str:
                if os.path.isfile(in_s):
                    # Load file
                    s = open(in_s, "r")
                else:
                    s = io.StringIO(in_s)
            else:
                raise Exception("Unknown argument \"%s\"" % str(in_s))

            scope = self._ast_f.mkGlobalScope(len(roots))

            ast_builder.build(scope, s)

            roots.append(scope)

            if hasattr(s, "close"):
                s.close()

            if marker_c.hasSeverity(zspp.MarkerSeverityE.Error):
                for m in marker_c.markers():
                    print("Marker: %s" % m.msg())
                    
                raise Exception("Errors while parsing %s" % name)

        ast_linker = self._zspp_f.mkAstLinker()

        root_symtab = ast_linker.link(marker_c, roots)

        if marker_c.hasSeverity(zspp.MarkerSeverityE.Error):
            for m in marker_c.markers():
                print("Marker: %s" % m.msg())

            raise Exception("Errors while linking %s" % name)

        zsp_arl_f = arl_dm.Factory.inst()
        ast2arl_ctxt = zsp_fe_parser.Factory.inst().mkAst2ArlContext(
            self.ctxt,
            root_symtab,
            marker_c)
        
        ast2arl_builder = zsp_fe_parser.Factory.inst().mkAst2ArlBuilder()
        ast2arl_builder.build(root_symtab, ast2arl_ctxt)

        if marker_c.hasSeverity(zspp.MarkerSeverityE.Error):
            if marker_c.hasSeverity(zspp.MarkerSeverityE.Error):
                for m in marker_c.markers():
                    print("Marker: %s" % m.msg())

            raise Exception("Errors while elaborating %s" % name)

        return self.ctxt



