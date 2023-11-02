#****************************************************************************
#* cmd_parse_base.py
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
import argparse
import ciostream
import zsp_arl_dm.core as arl_dm
import zsp_parser.core as zsp_parser
import zsp_fe_parser.core as fe_parser

class CmdParseBase(object):

    def __init__(self):
        pass

    def parseFilesToCtxt(self, files):
        parser_f = zsp_parser.Factory.inst()
        fe_parser_f = fe_parser.Factory.inst()
        arl_dm_f = arl_dm.Factory.inst()
        marker_c = parser_f.mkMarkerCollector()
        ast_f = parser_f.getAstFactory()
        ast_builder = parser_f.mkAstBuilder(marker_c)
        ast_roots = []

        lib = ast_f.mkGlobalScope(0)
        parser_f.loadStandardLibrary(ast_builder, lib)
        ast_roots.append(lib)

        for i,file in enumerate(files):
            glbl = ast_f.mkGlobalScope(i+1)
            with open(file, "r") as fp:
                ast_builder.build(glbl, fp)
            if marker_c.hasSeverity(zsp_parser.MarkerSeverityE.Error):
                break
            ast_roots.append(glbl)
        
        if marker_c.hasSeverity(zsp_parser.MarkerSeverityE.Error):
            raise Exception("Parsing failed")
        
        linker = parser_f.mkAstLinker()

        root_scope = linker.link(marker_c, ast_roots)

        if marker_c.hasSeverity(zsp_parser.MarkerSeverityE.Error):
            raise Exception("Linking failed")

        arl_ctxt = arl_dm_f.mkContext()
        ast2arl_ctxt = fe_parser_f.mkAst2ArlContext(
            arl_ctxt,
            root_scope,
            marker_c
        )
        ast2arl = fe_parser_f.mkAst2ArlBuilder()
        ast2arl.build(
            root_scope,
            ast2arl_ctxt
        )


        return arl_ctxt

    @staticmethod
    def addFileArgs(parser : argparse.ArgumentParser):
        parser.add_argument("files", nargs="+")

