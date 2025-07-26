from src import Relmap, Column, Table, propagate, render
graph = Relmap()
graph.generate_random_seeds()
propagate(graph)
model = graph.get_all_tables('model')[0]
print(render(model, graph))