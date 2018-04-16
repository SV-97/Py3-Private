geheimnis = 1337
versuch = -1
zaehler = 0

while versuch != geheimnis:
    versuch = int(input("Raten Sie: "))
    if versuch < geheimnis:
        print("Zu klein")

    if versuch > geheimnis:
        print("Zu groß")

    zaehler = zaehler +1

print("Super, Sie haben es in ", zaehler, "Versuchen geschafft!")