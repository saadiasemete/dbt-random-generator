import subprocess
import os
import shutil
from .randomness import randstr, random_piece_of_data
from .relmap import Relmap
from .table import Table
from .column import Column
from .settings import SEED_SIZE, jinja_env
from .renderer import render
from contextlib import chdir


def uses_directory(func):
    def wrapper(self: 'DbtProject', *args, **kwargs):
        with chdir(self.folder):
            return func(self, *args, **kwargs)
    return wrapper


class DbtProject:

    @uses_directory
    def cleanup(self):
        shutil.rmtree('models/example')
        # os.remove('models/schema.yml')

    # TODO: make something fancier
    @uses_directory
    def mock_profile(self):
        profiles = jinja_env.get_template(
            'profiles.yml').render(name=self.name)
        with open('profiles.yml', 'w', encoding='utf-8') as f:
            f.write(profiles)

    def __init__(self, name: str = None, folder: str = '.'):
        if name is None:
            name = randstr()
        folder = os.path.abspath(folder)
        with chdir(folder):
            self.name = name
            dbt_init = subprocess.run(
                ['dbt', 'init', '-s'],
                input=self.name,
                text=True,
                capture_output=True
            )
            if dbt_init.stderr:
                raise Exception(dbt_init.stderr)

        self.folder = os.path.join(folder, self.name)
        self.cleanup()
        self.mock_profile()

    @uses_directory
    def write_seed(self, seed: Table, columns: list[Column]):
        assert seed.kind == 'seed'
        with open(os.path.join(os.curdir, 'seeds', seed.name+'.csv'), mode='w') as f:
            f.write(','.join([column.name for column in columns]))
            f.write(os.linesep)
            for i in range(SEED_SIZE*len(columns)):
                col_index = i % len(columns)
                f.write(str(random_piece_of_data(columns[col_index].type)))
                f.write(',' if col_index+1 < len(columns) else os.linesep)

    def make_seeds(self, graph: Relmap):
        seeds = graph.get_all_tables(kind='seed')
        for seed in seeds:
            self.write_seed(
                seed=seed,
                columns=graph.get_model_columns(seed)
            )

    @uses_directory
    def write_model(self, model: Table, sql: str):
        assert model.kind == 'model'
        with open(os.path.join(os.curdir, 'models', model.name+'.sql'), mode='w') as f:
            f.write(sql)

    @uses_directory
    def make_models(self, graph: Relmap):
        models = graph.get_all_tables(kind='model')
        for model in models:
            self.write_model(
                model=model,
                sql=render(model, graph)
            )
