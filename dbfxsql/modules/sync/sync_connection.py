from dbfxsql.modules import dbf_controller, sql_controller


def insert(engine: str, filename: str, table: str, fields: tuple) -> None:
    if "DBF" == engine.upper():
        dbf_controller.insert_row(engine, filename, fields)

    else:
        sql_controller.insert_row(engine, filename, table, fields)


def read(engine: str, filename: str, table: str) -> dict:
    if "DBF" == engine.upper():
        return dbf_controller.read_rows(engine, filename, condition=None)

    return sql_controller.read_rows(engine, filename, table, condition=None)


def update(engine: str, filename: str, table: str, fields: tuple, index: int) -> None:
    condition: tuple = ("row_number", "==", f"{index + 1}")

    if "DBF" == engine.upper():
        dbf_controller.update_rows(engine, filename, fields, condition)

    else:
        sql_controller.update_rows(engine, filename, table, fields, condition)


def delete(engine: str, filename: str, table: str, index: int) -> None:
    condition: tuple = ("row_number", "==", f"{index + 1}")

    if "DBF" == engine.upper():
        dbf_controller.delete_rows(engine, filename, condition)

    else:
        sql_controller.delete_rows(engine, filename, table, condition)
