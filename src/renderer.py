from .table import Table
from .relmap import Relmap
from .column import Column
from sqlglot import expressions as exp


def render(model: Table, graph: Relmap) -> str:
    assert model.kind == 'model'
    columns = graph.get_model_columns(model)
    rendered_transformations: list[exp.Func] = []
    ancestors: set[Table] = set()

    for column in columns:
        transformation = graph.get_creating_transformation(column)
        args = graph.get_transformation_arguments(
            transformation=transformation)
        rendered_transformations.append(
            transformation.build_expr(
                args=[arg.to_sqlglot_column() for arg in args],
                alias = column.name
            )
        )
        ancestors.update(
            set([arg.table for arg in args if isinstance(arg, Column)]))

    # TODO: several ancestors & join logic

    ancestor = ancestors.pop()

    select_expr = exp.Select().select(
        *rendered_transformations
    ).from_(
        exp.Table(this=exp.Identifier(this=ancestor.dbt_ref()))
    ).as_(ancestor.name)

    return select_expr.sql()
