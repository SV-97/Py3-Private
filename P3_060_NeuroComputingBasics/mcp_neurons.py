class McpNeuron():
    """McCulloch-Pitts-Neuron
    Binary Neuron that fires if the sum of it's inputs exceeds a treshold value
    A single input on the inhibitor input prevents the neuron from firing

    Attributes:
        inhibitors (iterable): inhibitor inputs
        inputs (iterable): input nodes
        output (int): output value
        treshold (int): treshold value
    """
    def __init__(self, treshold):
        self.inhibitors = []
        self.inputs = []
        self.treshold = treshold
    
    @property
    def output(self):
        return 1 if sum(int(input) for input in self.inputs) >= self.treshold \
            and 1 not in (int(inhibitor) for inhibitor in self.inhibitors) else 0

    def __int__(self):
        return self.output


class McpAndGate(McpNeuron):
    def __init__(self):
        super().__init__(2)


class McpOrGate(McpNeuron):
    def __init__(self):
        super().__init__(1)


if __name__=="__main__":
    # and
    print("\nX = A and B")
    print(f"|{'A':^3}|{'B':^3}|{'X':^3}|")
    a_1 = McpAndGate()
    for A in range(2):
        for B in range(2):
            a_1.inputs = [A, B]
            assert(A & B == a_1.output)
            print(f"|{A:^3}|{B:^3}|{a_1.output:^3}|")

    # or
    print("\nX = A or B")
    print(f"|{'A':^3}|{'B':^3}|{'X':^3}|")
    a_1 = McpOrGate()
    for A in range(2):
        for B in range(2):
            a_1.inputs = [A, B]
            assert(A | B == a_1.output)
            print(f"|{A:^3}|{B:^3}|{a_1.output:^3}|")

    # and not
    print("\nX = A and not B")
    print(f"|{'A':^3}|{'B':^3}|{'X':^3}|")
    a_1 = McpNeuron(1)
    for A in range(2):
        for B in range(2):
            a_1.inputs = [A]
            a_1.inhibitors = [B]
            assert(A & ~B == a_1.output)
            print(f"|{A:^3}|{B:^3}|{a_1.output:^3}|")

    # xor
    print("\nX = A xor B")
    print(f"|{'A':^3}|{'B':^3}|{'X':^3}|")
    a_1 = McpNeuron(1)
    a_2 = McpNeuron(1)
    a_3 = McpOrGate()
    for A in range(2):
        for B in range(2):
            a_1.inputs = [A]
            a_1.inhibitors = [B]

            a_2.inputs = [B]
            a_2.inhibitors = [A]

            a_3.inputs = [a_1, a_2]
            assert(A ^ B == a_3.output)
            print(f"|{A:^3}|{B:^3}|{a_3.output:^3}|")

    # nand
    print("\nX = A nand B")
    print(f"|{'A':^3}|{'B':^3}|{'X':^3}|")
    a_1 = McpAndGate()
    a_2 = McpOrGate()
    for A in range(2):
        for B in range(2):
            a_1.inputs = [A, B]

            a_2.inputs = [A, B]
            a_2.inhibitors = [a_1]

            assert((A & ~B) | (~A & B) == a_2.output)
            print(f"|{A:^3}|{B:^3}|{a_2.output:^3}|")
