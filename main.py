from src.table import Table


seed = Table.generate_seed()
graph = Table.generate_seed().represent_as_graph()
print(graph)
