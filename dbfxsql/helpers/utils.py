import types

from dbfxsql.constants import sample_commands
from dbfxsql.helpers import file_manager, formatters

from prettytable import PrettyTable


def show_table(rows: list[dict]) -> None:
    """Displays a list of rows in a table format."""

    table = PrettyTable()

    table.field_names = rows[0].keys() if rows else []

    for row in rows:
        table.add_row([row[field] for field in table.field_names])

    print(table, end="\n\n")


def embed_examples(func: types.FunctionType) -> types.FunctionType:
    """Decorator to add docstrings to a function."""
    examples: str = """
    \n
    \b
    Examples:
    ---------
    """

    for command in sample_commands.DBF.keys():
        if func.__name__ in command:
            examples += "- " + sample_commands.DBF[command]

    for command in sample_commands.SQL.keys():
        if func.__name__ in command:
            examples += "\n    "
            examples += "- " + sample_commands.SQL[command]

    func.__doc__ += examples

    return func


def notify(operations: list, tables: list) -> None:
    for operation, table in zip(operations, tables):
        if operation["insert"] or operation["update"] or operation["delete"]:
            message: str = f"\nMake changes in: {table.source}"
            print(message if not table.name else message + f" > {table.name}")

            for row in operation["insert"]:
                print(f"Insert row: {row["fields"]}")

            for row in operation["update"]:
                print(f"Update row: {row["fields"]} with row_number {row["index"]}")

            for row in operation["delete"]:
                print(f"Delete row with row_number {row["index"]}")


def check_engine(filename: str) -> str | None:
    extension: str = formatters.decompose_file(filename)[1]
    engines: dict = file_manager.load_config()["engines"]

    for engine_name, engine_config in engines.items():
        if extension in engine_config["extensions"]:
            return engine_name
