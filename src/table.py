from .column import Column
from .utils import randstr
import networkx as nx 
import random

class Table:


    def __init__(self, name: str, kind: str, **kwargs):
        self.name = name 
        self.kind = kind
    
    def __repr__(self):
        return self.name
    
    def __hash__(self):
        return hash(self.name)


        