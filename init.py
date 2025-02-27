import db_utils

NAME_LIST = [
    {"name": "Maria", "age": 20},
    {"name": "Carlos", "age": 21},
    {"name": "Pedro", "age": 18},
    {"name": "Sofia", "age": 19},
]

for p in NAME_LIST:
    db_utils.insert_into_db("people", p)
