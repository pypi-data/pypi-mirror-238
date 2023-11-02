#****************************************************************************
#* seq_eval_iterator_processor.py
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

import asyncio
import zsp_arl_dm.core as arl_dm
from zsp_arl_dm.core import ExecKindT


class SeqEvalIteratorProcessor(object):

    def __init__(self, pss_top):
        self.pss_top = pss_top

    def process(self, eval_it : arl_dm.ModelEvalIterator):

        if eval_it.next():
            self._process_item(eval_it)

    def _process_item(self, eval_it):
        print("_process_item: kind=%s" % eval_it.type())

        if eval_it.type() == arl_dm.ModelEvalNodeT.Action:
            is_compound = self.process_action(eval_it.action())

            if is_compound:
                # Following sequence is the body

                print("compound kind=%s" % eval_it.type())

                activity_it = eval_it.iterator()
                activity_it.next()
                self._process_item(activity_it)

        elif eval_it.type() == arl_dm.ModelEvalNodeT.Sequence:
            self.process_sequence(eval_it.iterator())
        elif eval_it.type() == arl_dm.ModelEvalNodeT.Parallel:
            self.process_parallel(eval_it.iterator())
        else:
            raise Exception("Unknown eval node type %s" % eval_it.type())

    def process_action(self, action : arl_dm.ModelFieldAction):
        is_compound = action.isCompound()

        print("Action: %s is_compound=%s" % (action.name(), is_compound))

        if not is_compound:
            action_facade = action.getFieldData()

            asyncio.get_event_loop().run_until_complete(action_facade._evalExecTarget(ExecKindT.Body))

        return is_compound

    def process_parallel(self, eval_it : arl_dm.ModelEvalIterator):

        while eval_it.next():
            print("Branch: %s" % eval_it.type())
            # Process a branch

            self._process_item(eval_it)

    def process_sequence(self, eval_it : arl_dm.ModelEvalIterator):
        print("process_sequence")

        while eval_it.next():
            self._process_item(eval_it)
