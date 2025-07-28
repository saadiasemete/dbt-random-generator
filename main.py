from src import Relmap, Column, Table, propagate, render, DbtProject
graph = Relmap()
graph.generate_random_seeds()
propagate(graph)
model = graph.get_all_tables('model')[0]
print(render(model, graph))
dbt = DbtProject(folder='output')
dbt.make_seeds(graph)
dbt.make_models(graph)