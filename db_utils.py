"""
Operaciones donde usamos la base de datos. No se usar bases de datos.

Por Hapurobokka.
"""

import sqlite3

DATABASE = "db/test.db"


def run_query(query, parameters=()) -> sqlite3.Cursor:
    """Runs a query for the external database"""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        result = cursor.execute(query, parameters)
        conn.commit()
    return result


def request_data(query, parameters=()) -> list[tuple]:
    """Queries the database for the solicited information, then returns a list of tuples"""
    some_cursor = run_query(query, parameters)
    return some_cursor.fetchall()


def comma_separated_string(lst: list) -> str:
    """Takes a list as an argument. Joins all of it's elements with a comma and space"""
    values_string = ", ".join(lst)

    return values_string


def create_query_placeholder(lst: list[str]) -> str:
    values_string = []
    for string in lst:
        values_string.append(f"{string} = ?")

    return ", ".join(values_string)


def create_values_string(times, char="?"):
    """
    Devuelve una string que contiene char la cantidad de veces indicada por times
    """
    char_list = []
    for _ in range(times):
        char_list.append(char)
    return ", ".join(char_list)


def create_insert_query(table, table_fields):
    """Crea una query apropiada para introducir valores en una tabla"""

    return f"""
    INSERT INTO {table} ({comma_separated_string(table_fields)})
    VALUES ({create_values_string(len(table_fields))})
    """


def create_record(table, table_fields, values):
    """Crea una entrada en la tabla indicada usando los valores pasados como argumento"""
    query = create_insert_query(table, table_fields)
    run_query(query, values)


def insert_into_db(table: str, data: dict):
    """Takes a dictonary and builds a query from it and uses it to insert the values"""
    table_fields = list(data.keys())
    table_values = list(data.values())

    create_record(table, table_fields, table_values)
        

def delete_record(table, key, value):
    """Borra una entrada de una tabla utilizando su ID"""
    run_query(f"DELETE FROM {table} WHERE {key} = {value}")


def tuples_to_vector(some_tuples):
    """
    Toma una lista de tuplas y devuelve una lista que contiene solo el primer valor de todas
    ellas"""
    return [tup[0] for tup in some_tuples]


def get_total_amount(table, selection, register_id):
    """Queries the database for a list of values and then adds them all"""
    query = f"SELECT {selection} FROM {table} WHERE register_id = ?"
    values = request_data(query, (register_id,))

    if not values:
        return 0

    return sum(tuples_to_vector(values))


def get_id(table, field, value):
    """Gets an id from the database"""
    db_id = request_data(f"SELECT id FROM {table} WHERE {field} = ?", (value,))

    try:
        return db_id[0][0]
    except IndexError:
        return None
