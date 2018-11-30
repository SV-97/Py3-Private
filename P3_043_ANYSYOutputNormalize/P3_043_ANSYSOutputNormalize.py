from os import path
from pathlib import Path

path = Path(path.dirname(__file__))

origin = input("Origin filename: ")
with open(path / origin, "r") as f_origin:
    with open(path / ("normalized_" + origin), "w") as f_new:
        for line in f_origin:
            try:
                newline = line.replace("\n", "")
                while "  " in newline:
                    newline = newline.replace("  ", " ")
                newline = newline.rstrip(" ").lstrip(" ")
                s1, s2_2 = newline.split(" ")
                s1 = float(s1)
                s2_2 = float(s2_2)
                newline = f"{s1:<15.6E} {s1:<15.6E}\r\n"
                f_new.write(newline)
            except ValueError:
                continue
