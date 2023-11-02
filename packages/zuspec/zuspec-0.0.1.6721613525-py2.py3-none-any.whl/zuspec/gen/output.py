#****************************************************************************
#* output.py
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

class Output(object):

    def __init__(self, out=None):
        if out is not None:
            self._out = out
        else:
            self._out = io.StringIO()
        self._ind = ""
        self._comma = []

    def getvalue(self):
        if hasattr(self._out, "getvalue"):
            return self._out.getvalue()
        else:
            raise Exception("Not operating on a string")
        
    def push_comma(self, c):
        self._comma.append(c)

    def pop_comma(self):
        self._comma.pop()

    def comma(self):
        return "," if len(self._comma) > 0 and self._comma[-1] else ""

    def println(self, s=""):
        self._out.write(self._ind)
        self._out.write(s)
        self._out.write("\n")

    def write(self, s):
        self._out.write(s) 
    
    def inc_ind(self):
        self._ind += "    "

    def ind(self):
        return self._ind
    
    def dec_ind(self):
        if len(self._ind) > 4:
            self._ind = self._ind[4:]
        else:
            self._ind = ""


