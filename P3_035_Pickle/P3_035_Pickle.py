import pickle
import tempfile

class Jar():
    def __init__(self, vegetable, amount):
        self.vegetable = vegetable
        self.amount = amount
    def take_one_out(self):
        self.amount -= 1
        return self.amount
    def __str__(self):
        return "Jar with {} {}s".format(self.amount, self.vegetable)

for i in range(5):
    with tempfile.TemporaryFile() as f:
        print("""
{}
        """.format(i))
        p = pickle.Pickler(f, i)
        jar = Jar("Pickle", 10)
        p.dump("It were {} {}s".format(jar.take_one_out(), jar.vegetable))
        p.dump(jar)
        f.flush()
        f.seek(0)
        for line in f.readlines():
            print(line)
        f.seek(0)
        up = pickle.Unpickler(f)
        print("Unpickled:    {}".format(up.load()))
        the_old_jar = up.load()
        print("Unpickled:    {}".format(the_old_jar.take_one_out()))