from src import Relmap, Column, Table, propagate
graph = Relmap()
graph.generate_random_seeds()
propagate(graph)