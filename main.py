from src import Relmap, propagate


for i in range(100):
    graph = Relmap()
    graph.generate_random_seeds()
    propagate(graph)

    assert len(graph.get_all_tables()) == 2
    print(f'OK: {i}')