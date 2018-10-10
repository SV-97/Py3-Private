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

def find_previous_prime(n):
    while True:
        n -= 1
        bools = []
        for i in range(2, n):
            bools.append(bool(n%i))
        if not (False in bools):
            return n

def primes_in_range(end, file="Primes"):
    """Sieve of Eratosthenes
    Find all primes in a given range
    """
    range_ = list(range(3, end+1, 2))
    range_.insert(0, 2)
    primes = []
    counter = 0
    with open(file, "w+") as f:
        try:
            highest_in_file = int(get_last_line(f)[11:], base=16)
            last_in_range = find_previous_prime(2_000_000)
            print(highest_in_file)
            print(last_in_range)
            if highest_in_file == last_in_range:
                primes = [int(line[11:], base=16) for line in f]
                return primes
        except ValueError:
            pass

        for i in range_[:]:
            if i in range_:
                primes.append(i)
                print(i)
                f.write("0x{:0>8}|0x{:0>8}\n".format(hex(counter)[2:], hex(i)[2:]))
                f.flush()
                counter += 1
                n_multiples = end//i if i%2 else False # how many multiples of i are in range(end)
                if not n_multiples:
                    continue
                multiples = [i*j for j in range(i, n_multiples+1, 2) if i*j in range_]
                range_ = [x for x in range_ if x not in multiples]
    return primes
