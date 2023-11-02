#****************************************************************************
#* my_class.py
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
#from .loader import *
#from .zuspec import *
from .runner import Runner
from .actor import Actor
from .env_config import EnvConfig

def _init():
    """Initializes libraries used by Zuspec"""
    pass

_init()

def loadContextFromPSS(*args, **kwargs):
    import zsp_arl_dm.core as arl_dm
    import zsp_fe_parser.core as zsp_fe_parser
    import zsp_parser.core as zspp

    zspp_f = zspp.Factory.inst()
    ast_f = zspp_f.getAstFactory()

    ctxt = arl_dm.Factory.inst().mkContext()

    marker_c = zspp_f.mkMarkerCollector()

    ast_builder = zspp_f.mkAstBuilder(marker_c)

    roots = []

    # First, load up the core package

    scope = ast_f.mkGlobalScope(len(roots));
    zspp_f.loadStandardLibrary(
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

        scope = ast_f.mkGlobalScope(len(roots))
        ast_builder.build(scope, s)
        roots.append(scope)

        if hasattr(s, "close"):
            s.close()

        if marker_c.hasSeverity(zspp.MarkerSeverityE.Error):
            raise Exception("Errors while parsing %s" % name)

    ast_linker = zspp_f.mkAstLinker()
    root_symtab = ast_linker.link(marker_c, roots)

    if marker_c.hasSeverity(zspp.MarkerSeverityE.Error):
        raise Exception("Errors while parsing %s" % name)

    zsp_arl_f = arl_dm.Factory.inst()
    ast2arl_ctxt = zsp_fe_parser.Factory.inst().mkAst2ArlContext(
        ctxt,
        marker_c)
       
    ast2arl_builder = zsp_fe_parser.Factory.inst().mkAst2ArlBuilder()
    ast2arl_builder.build(root_symtab, ast2arl_ctxt)

    if marker_c.hasSeverity(zspp.MarkerSeverityE.Error):
        raise Exception("Errors while parsing %s" % name)

    return ctxt

def mkSingleExecutorEvalActionIter(
        ctxt,
        randstate,
        comp, 
        action): 
    import zsp_arl_dm.core as arl_dm
    import zsp_arl_eval.core as zsp_arl_eval
    import vsc_solvers.core as vsc_solvers

    zsp_eval_f = zsp_arl_eval.Factory.inst()

    eval = zsp_eval_f.mkModelEvaluator(
        zsp_arl_eval.ModelEvaluatorKind.FullElab,
        vsc_solvers.Factory.inst(),
        ctxt)
    
    comp_t = ctxt.findDataTypeComponent(comp)
    if comp_t is None:
        raise Exception("Failed to find component %s" % comp)

    action_t = ctxt.findDataTypeAction(action)
    if action_t is None:
        raise Exception("Failed to find action %s" % action)

    builder_ctxt = arl_dm.ModelBuildContext(ctxt)
    comp_model = comp_t.mkRootField(
        builder_ctxt,
        "pss_top",
        False)


    eval_it = eval.eval(
        randstate,
        comp_model,
        action_t
    )

    return eval_it 

def mkDotGraph(
        ctxt,
        randstate,
        comp,
        action):
    import zsp_arl_dm.core as arl_dm
    import zsp_arl_eval.core as zsp_arl_eval
    import vsc_solvers.core as vsc_solvers
    from .impl.generator_dot import GeneratorDot

    zsp_eval_f = zsp_arl_eval.Factory.inst()

    eval = zsp_eval_f.mkModelEvaluator(
        zsp_arl_eval.ModelEvaluatorKind.FullElab,
        vsc_solvers.Factory.inst(),
        ctxt)
    
    comp_t = ctxt.findDataTypeComponent(comp)
    if comp_t is None:
        raise Exception("Failed to find component %s" % comp)

    action_t = ctxt.findDataTypeAction(action)
    if action_t is None:
        raise Exception("Failed to find action %s" % action)

    builder_ctxt = arl_dm.ModelBuildContext(ctxt)
    comp_model = comp_t.mkRootField(
        builder_ctxt,
        "pss_top",
        False)

    dotgen = GeneratorDot(comp_model)

    eval_it = eval.eval(
        randstate,
        comp_model,
        action_t)
    
    return dotgen.gen(eval_it)
