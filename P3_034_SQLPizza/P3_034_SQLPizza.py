import sqlite3

connection = sqlite3.connect(":memory:")
cursor = connection.cursor()

cursor.execute("""CREATE TABLE kunde (
    kundenid INTEGER, vorname TEXT, nachname TEXT, strasse TEXT)""")
cursor.execute("""CREATE TABLE bestellung (
    bestellnr INTEGER, kundenid INTEGER, lieferid INTEGER)""")
cursor.execute("""CREATE TABLE lieferanten (
    lieferid INTEGER, vorname TEXT, nachname TEXT)""")
cursor.execute("""CREATE TABLE pizzasorte (
    listenid INTEGER, bezeichnung TEXT)""")

sorten = ("Salami", "Schokolade", "Spezial", "Diavolo", "Texas")
cursor.executemany("INSERT INTO pizzasorte VALUES (?, ?)", enumerate(sorten))
kundenvornamen = ("Schoko", "Gummi", "Grizzly")
kundennachnamen = tuple(["Bär" for i in range(len(kundenvornamen))])
strassen = ("Gummistraße", "Schokostraße", "Straßenstraße")
kundendaten = tuple(zip(range(len(kundenvornamen)), kundenvornamen, kundennachnamen, strassen))
cursor.executemany("INSERT INTO kunde VALUES (?, ?, ?, ?)", kundendaten)

cursor.execute("SELECT * FROM pizzasorte")
print(cursor.fetchall())
cursor.execute("SELECT * FROM kunde")
print(cursor.fetchall())