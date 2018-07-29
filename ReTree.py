# -*- coding: utf-8 -*-
"""
@author: Dave
"""
import re
import numpy as np
import Helpers 

class Node(object):
    def __init__(self, level, data = [], ):
        self.level = level
        self.data = data
        #self.re_prefix = '.{%d}' % (level-1) 
        self.re_prefix = ''
        self.re = ''

class Root(Node):
    def __init__(self, data = []):
        super().__init__(level = 0, data = data)
        self.left = None
        self.right = None
        self.re_prefix = ''
        
class InternalNode(Node):
    def __init__(self, level, parent,  data = []):
        super().__init__(level, data)
        self.parent = parent
        self.left = None
        self.right = None
        
    def is_left_child(self):
        return self.parent.left == self
    def is_right_child(self):
        return self.parent.right == self
        
        
class TerminalNode(Node):
    def __init__(self, level, data, parent, re ):
        super().__init__(level, data)
        self.parent = parent
        self.re = re
        
class ReTree(object):

    def __init__(self, data, max_height = 7, re_file = None):
        self.data = data
        self.tree = Root(data = self.data)
        self.max_height = max_height
        self.re_file = re_file
        self.terminal_node_list = []
        
    def build(self, node = None, regexps = ''):
        if self.re_file:
            if not node: 
                self.build_from_file(self.tree, Helpers.load_csv(self.re_file))
            else:
                self.buidl_from_file(node, regexps)
        else:
            self.build_gen(self.tree)
            
    
    def build_from_file(self, node, regexps):
        re_gini = {}
        
        for regexp in regexps:
            re_gini[regexp] = self.gini_index(node.data, regexp)
            
        if len(re_gini):
            min_re = min(re_gini, key=re_gini.get)
            node.re = min_re
            regexps.remove(min_re)
            
        if node.level != self.max_height - 1 and len(re_gini) and re_gini[min_re] != 0 :
            self.split(node)
            self.build_from_file(node.left)
            self.build_from_file(node.right)
        else:
            self.to_terminal(node)
    
    def build_gen(self, node):
        node.re, gini = self.generate_re(node.data, node.re_prefix) 
        if node.level != self.max_height - 1 and gini != 0 :
            self.split(node)
            self.build_gen(node.left)
            self.build_gen(node.right)
        else:
            self.to_terminal(node)
        
            
    def to_terminal(self, node):
        if(node.is_left_child()):
            node.parent.left = TerminalNode(node.level, node.data, node.parent, node.re)
        elif(node.is_right_child()):
            node.parent.right = TerminalNode(node.level, node.data, node.parent, node.re)
    
    def split(self, node):
        left = []
        right = []
        
        for row in node.data:
            if re.match(node.re_prefix + node.re, row[0]):
                right.append(row)
            else:
                left.append(row)
                
        node.left = InternalNode(node.level +1, node, left)
        node.right = InternalNode(node.level +1, node,  right)
        
    
    def gini_index(self, data, regex):
        gr1_cl1, gr1_cl0, gr2_cl1, gr2_cl0 = (0, 0, 0 ,0) 
        d = len(data)
        
        for line, cl in data:
            if re.match(regex, line):
                if cl:
                    gr1_cl1 += 1
                else:
                    gr1_cl0 += 1
            else:
                if cl:
                    gr2_cl1 += 1
                else:
                    gr2_cl0 += 1
        if d == 0:
            return 0
        else:
            gini_gr1 = (1-((gr1_cl1/d)**2 + ((gr1_cl0/d)**2))) * (gr1_cl1 + gr1_cl0)/d
            gini_gr2 = (1-((gr2_cl1/d)**2 + ((gr2_cl0/d)**2))) * (gr2_cl1 + gr2_cl0)/d
            
        return gini_gr1 + gini_gr2
        
    
            
    def generate_re(self, data, prefix):
        options = ('A', 'G', 'T', 'C')
        ginis = []
        alternatives = tuple(Helpers.generate_alternatives(options))
        regexps = options + alternatives
        for reg in regexps:    
            ginis.append(self.gini_index(data, prefix + reg))
        return regexps[np.argmin(ginis)], min(ginis)
        
    
    #def prune(self, data):
        #for x in range(0,len(self.terminal_node_list), 2):
            
        
    def find_terminal_nodes(self, node):
        if(type(node) != TerminalNode):
            self.find_terminal_nodes(node.left)
            self.find_terminal_nodes(node.right)
        else:
            self.terminal_node_list.append(node)
        
    def match(self, node, string):
        return re.match(node.re_prefix + node.re, string)
    
    def classify(self, string):
        node = self.tree
        while(type(node) is not TerminalNode):
            if(self.match(node, string)):
                node = node.right
            else: 
                node = node.left
        return 0 if not self.match(node, string) else 1