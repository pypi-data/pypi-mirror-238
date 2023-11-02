#****************************************************************************
#* runner.py
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

import vsc_solvers.core as vsc_solvers

class Ctxt(object):

    _inst = None

    def __init__(self):
        self._ctxt = None
        self._backend = None
        self._seed = None

    def init(self):
        import vsc_solvers.core as vsc_solvers
        from vsc_dataclasses.impl import Ctor as VscCtor
        from zsp_dataclasses.impl import Ctor as ZspCtor
        import zsp_arl_dm.core as arl_dm

        self._ctxt = arl_dm.Factory.inst().mkContext()
        self._seed = vsc_solvers.Factory.inst().mkRandState("0")

        ZspCtor.init(self._ctxt)
        VscCtor.init(self._ctxt)

        pass

    def setState(self, s):
        self._seed = s

    def nextState(self):
        return self._seed.next()

    @property
    def ctxt(self):
        return self._ctxt
    
    @property
    def backend(self):
        return self._backend
    
    @backend.setter
    def backend(self, v):
        self._backend = v

    @classmethod
    def inst(cls):
        if cls._inst is None:
            cls._inst = Ctxt()
            cls._inst.init()
        return cls._inst