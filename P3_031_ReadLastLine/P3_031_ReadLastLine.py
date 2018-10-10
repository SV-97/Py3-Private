with open("File", "w") as f:
    f.writelines([str(i)+"\n" for i in range(20)])
    print(type(f))

def get_last_line(f, newline="\n"):
    """Get last line of text in file
    Args:
        f (_io.TextIOWrapper): File to search in
        newline (str): escape character for the newline used
    Returns:
        Last line of file with stripped newline
    """
    f.seek(0, 2)
    f.seek(f.tell()-1, 0)
    a = None
    while a != newline:
        pos = f.tell()
        f.seek(pos-1, 0)
        a = f.read(1)
        f.seek(pos-1, 0)
    f.seek(f.tell()+1)
    last = f.readline().rstrip(newline)
    return last

with open("File", "r") as f:
    first = f.readline().rstrip("\n")
    print(first)
    print(get_last_line(f))
