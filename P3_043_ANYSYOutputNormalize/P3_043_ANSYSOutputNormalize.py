from os import path as os_path
from pathlib import Path

while True:
    path = Path(input("Enter path to file(with file) or leave empty for relative pathname: "))
    if not path:
        path = Path(os_path.dirname(__file__))
        origin = input("Origin filename: ")
    else:
        origin = path.name
        path = path.parent

    try:
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
                        newline = f"{s1:+< 15.6E} {s2_2:< 15.6E}\r\n"
                        f_new.write(newline)
                    except ValueError:
                        continue
    except Exception as e:
        print(e)
    else:
        print("Finished succesfully!")
    if not input("Enter something to read another file: "):
        break
input("Press return to continue...")