#****************************************************************************
#* cmd_registry.py
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

class CmdRegistry(object):

    _inst = None

    def __init__(self):
        self._subcmd_factory_m = {}
        self.addSubCommand("synth", self._addSynthCommand)
        pass

    def addSubCommand(self, name, factory):
        if name in self._subcmd_factory_m.keys():
            raise Exception("Attempting to register duplicate command %s" % name)
        self._subcmd_factory_m[name] = factory

    def getParser(self):
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers()
        subparsers.required = True

        for key,value in self._subcmd_factory_m.items():
            value(key, subparsers)

        return parser

    def _addSynthCommand(self, name, subparsers):
        synth_cmd = subparsers.add_parser("synth",
            help="Process PSS and generate synthesized output")
        synth_cmd.add_argument("style", 
            choices={"c-test", "c-actions"},
            help="Specifies output generator")
        synth_cmd.set_defaults(func=None)
        synth_cmd.add_argument("args", nargs=argparse.REMAINDER)
        return synth_cmd

    @classmethod
    def inst(cls):
        if cls._inst is None:
            cls._inst = CmdRegistry()
        return cls._inst

