import re
from mcp_neurons import McpNeuron


class SymbolTable():
    def __init__(self):
        self.title = "Title"
        self.inputs = {}
        self.outputs = {}
        self.neurons = {}

    def __getitem__(self, index):
        if index in self.neurons.keys():
            return self.neurons[index]
        if index in self.outputs.keys():
            return self.outputs[index]
        if index in self.inputs.keys():
            return self.inputs[index]

    def __setitem__(self, index, item):
        if type(item) is Output:
            self.outputs[index] = item
            return
        if type(item) is Input:
            self.inputs[index] = item
            return
        self.neurons[index] = item
        return


class Output(McpNeuron):
    def __init__(self):
        super().__init__(0)


class Input(McpNeuron):
    def __init__(self):
        super().__init__(0)


class Parser():
    Title = re.compile(r"^title: (?P<title>(\S ?)+)")
    In = re.compile(r"^in: (?P<inputs>(\S(?!\-) ?)+)")
    Out = re.compile(r"^out: (?P<outputs>(\S(?!\-) ?)+)")
    Link = re.compile(r"^(?P<left>(\S(?!\-) ?)+) -- (?P<right>(\S(?!\-) ?)+)")
    Inhibition = re.compile(r"^(?P<left>(\S(?!\-) ?)+) -o (?P<right>(\S(?!\-) ?)+)")
    NeuronDecl = re.compile(r"^(?P<name>(\S(?!\-) ?)+): (?P<value>\d+)")

    def __init__(self, source, symbol_table):
        self.source = source.split("\n")
        self.symbol_table = symbol_table
        self.line_counter = 0

    def __iter__(self):
        self.source_iter = iter(self.source)
        return self

    def parse(self):
        for i in self: pass

    def __next__(self):
        cls = self.__class__
        line = next(self.source_iter)
        self.line_counter += 1
        inputs = cls.In.search(line)
        if inputs is not None:
            for name in inputs.group("inputs").split(" "):
                self.symbol_table[name] = Input()
            return

        outputs = cls.Out.search(line)
        if outputs is not None:
            for name in outputs.group("outputs").split(" "):
                self.symbol_table[name] = Output()
            return

        neuron_decl = cls.NeuronDecl.search(line)
        if neuron_decl is not None:
            neuron = McpNeuron(neuron_decl.group("value"))
            self.symbol_table[neuron_decl.group("name")] = neuron
            return

        link = cls.Link.search(line)
        if link is not None:
            left = self.symbol_table[link.group("left")]
            right = self.symbol_table[link.group("right")]
            right.inputs.append(left) # fails if right is input - this is wanted
            return

        inhibition = cls.Inhibition.search(line)
        if inhibition is not None:
            left = self.symbol_table[inhibition.group("left")]
            right = self.symbol_table[inhibition.group("right")]
            right.inhibitors.append(left) # fails if right is input - this is wanted
            return

        title = cls.Title.search(line)
        if title is not None:
            title = title.group("title")
            self.symbol_table.title = title
            return

        if re.search(r"(\s|\v)*", line): # skip empty lines, newlines etc
            return next(self)

        raise SyntaxError(f"Invalid Syntax in line {self.line_counter}: {line}")


class Writer():
    def __init__(self, symbol_table, target):
        self.table = symbol_table
        self.target = target

    def write(self):
        with open(self.target, "w") as f:
            indent = "    "
            f.write("""
digraph G {
    compound = true;
    labelloc = "t";\n"""
f"    label = <<B>{self.table.title}</B>>;\n"
"    edge [arrowhead=none];\n")
            for name, inp in self.table.inputs.items(): # declarations
                f.write(f"{indent}{id(inp)} [label=\"{name}\", shape=plain];\n")
            for name, outp in self.table.outputs.items():
                f.write(f"{indent}{id(outp)} [shape=plain, label=\"{name}\\nS={outp.treshold}\"];\n")
            for name, neuron in self.table.neurons.items():
                f.write(f"{indent}{id(neuron)} [label=\"S={neuron.treshold}\"];\n")

            for item in self.table.outputs.values(): # output links and inhibitions
                for link in item.inputs:                
                    f.write(f"{indent}{id(link)} -> {id(item)};\n")
                for inhibitor in item.inhibitors:                
                    f.write(f"{indent}{id(inhibitor)} -> {id(item)} [arrowhead=odot];\n")

            for item in self.table.neurons.values(): # inner neurons links and inhibitions
                for link in item.inputs:                
                    f.write(f"{indent}{id(link)} -> {id(item)};\n")
                for inhibitor in item.inhibitors:                
                    f.write(f"{indent}{id(inhibitor)} -> {id(item)} [arrowhead=odot];\n")
            
            f.write("}\n")
                


with open("descriptor.desc", "r") as f:
    text = f.read()

symbol_table = SymbolTable()
parser = Parser(text, symbol_table)
parser.parse()

writer = Writer(symbol_table, "target.dot")
writer.write()
