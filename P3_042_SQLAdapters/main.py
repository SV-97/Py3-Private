import sqlite3

import adapters
from classes import User

connection = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES)
cursor = connection.cursor()

user_1 = User("Bob", 12)

cursor.execute(\
"""
CREATE TABLE user(
    userobject USER
)
""")

cursor.execute(\
"""
INSERT INTO user VALUES (
    ?
)
""", (user_1,))

cursor.execute(\
"""
SELECT userobject 
FROM user
""")

itshim_1 = cursor.fetchall()[0][0]
print(itshim_1)