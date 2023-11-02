#****************************************************************************
#* generator_dot.py
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

import zsp_arl_dm.core as arl_dm

class GeneratorDot(arl_dm.VisitorBase):

    def __init__(self, pss_top):
        self.pss_top = pss_top
        self.output = ""
        self.ind = ""
        self._node_id = 0
        self._last_node_id = 0
        self._cluster_id = 0
        self._scope_s = []
        pass

    def gen(self, eval_it : arl_dm.ModelEvalIterator):
        self.output = ""

        node = self.node_id

        self.println("digraph A {")
        self.inc_ind()
        self.println("n%d[label=\"start\"];", node)

        self._last_node_id = node

        if eval_it.next():
            self._process_item(eval_it)

        node = self.node_id

        self.println("n%d[label=\"end\"];", node)
        self.println("n%d -> n%d;", self._last_node_id, node)
        self.dec_ind()
        self.println("}")

        return self.output

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

                # Now, close out the compound scope
                self.dec_ind()
                self.println("}")
                self.println("n%d -> n%d;", 
                    self._last_node_id,
                    self._scope_s[-1][1])
                self._last_node_id = self._scope_s[-1][1]
                self._scope_s.pop()

        elif eval_it.type() == arl_dm.ModelEvalNodeT.Sequence:
            self.process_sequence(eval_it.iterator())
        elif eval_it.type() == arl_dm.ModelEvalNodeT.Parallel:
            self.process_parallel(eval_it.iterator())
        else:
            raise Exception("Unknown eval node type %s" % eval_it.type())

    def inc_ind(self):
        self.ind += "    "

    def dec_ind(self):
        if len(self.ind) > 4:
            self.ind = self.ind[4:]
        else:
            self.ind = ""

    def println(self, fmt, *args):
        self.output += self.ind
        self.output += fmt % args
        self.output += "\n"

    @property
    def node_id(self):
        ret = self._node_id
        self._node_id += 1
        return ret

    @property
    def cluster_id(self):
        ret = self._cluster_id
        self._cluster_id += 1
        return ret

    def process_action(self, action : arl_dm.ModelFieldAction):
        is_compound = action.isCompound()

        print("Action: %s is_compound=%s" % (action.name(), is_compound))

        if is_compound:
            sid = self.node_id
            eid = self.node_id
            cid = self.cluster_id

            self.println("n%d -> n%d", self._last_node_id, sid)

            self.println("subgraph cluster%d {", cid)
            self.inc_ind();

            self.println("label=\"%s\";", action.name())
            self.println("n%d[shape=point,color=black];", sid)
            self.println("n%d[shape=point,color=black];", eid)

            self._scope_s.append((sid, eid))
            self._last_node_id = sid
        else:
            node = self.node_id
            label = action.name()

            self.println("n%d[label=\"%s\"];", node, label)

            self.println("n%d -> n%d;", self._last_node_id, node)
            self._last_node_id = node

        return is_compound

    def process_parallel(self, eval_it : arl_dm.ModelEvalIterator):
        sid = self.node_id
        eid = self.node_id
        self.println("n%d[shape=rectangle,width=1.0,height=0.05,label=\"\",style=filled];", sid)
        self.println("n%d[shape=rectangle,width=1.0,height=0.05,label=\"\",style=filled];", eid)

        if self._last_node_id:
            self.println("n%0d -> n%0d;", self._last_node_id, sid)

        self._scope_s.append((sid, eid))
        self._last_node_id = sid

        while eval_it.next():
            print("Branch: %s" % eval_it.type())
            # Process a branch
            self._last_node_id = self._scope_s[-1][0] # Start node

            self._process_item(eval_it)

            # Close out a branch by connecting the last 
            # action to the close bar
            self.println("n%0d -> n%0d;", 
                self._last_node_id,
                self._scope_s[-1][1])
            
        self._last_node_id = self._scope_s[-1][1]
        self._scope_s.pop()

        pass

    def process_sequence(self, eval_it : arl_dm.ModelEvalIterator):
        print("process_sequence")

        while eval_it.next():
            self._process_item(eval_it)

    def visitModelFieldComponent(self, c : arl_dm.ModelFieldComponent):
        pass


