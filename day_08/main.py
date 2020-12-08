from copy import deepcopy

class Console:
    def __init__(self):
        self.program = None 
        self.pc = 0
        self.acc = 0
        self.visted = []
        self.halt = False

    def __str__(self):
        return "PC: {}\nAccumaltor: {}\nRunning: {}".\
                format(self.pc, self.acc, not self.halt)

    def load_from_file(self, code_path): 
        with open(code_path) as f:
            self.program = [x.strip().split() for x in f.readlines()]

    def load_from_list(self, list_code):
        self.program = list_code

    def execute(self, prevent_loop = False):
        instruction = self.program[self.pc][0]
        if instruction == "nop":
            self.pc = self.pc + 1
        elif instruction == "acc":
            self.acc = self.acc + int(self.program[self.pc][1])
            self.pc = self.pc + 1
        elif instruction == "jmp": 
            self.pc = self.pc + int(self.program[self.pc][1])
        else:
            raise Exception("Unknown instruction: {}".format(instruction))
        if self.pc == len(self.program):
            self.halt = True

    def run_no_loops(self, verbose = True):
        while not self.halt:
            self.execute(True)
            if self.pc in self.visted:
                break
            self.visted.append(self.pc)

def FixCode(code_path):
    with open(code_path) as f:
        program = [x.strip().split() for x in f.readlines()]

    for idx in range(len(program)):
        if program[idx][0] == "acc":
            continue
        elif program[idx][0] == "nop":
            temp_program = deepcopy(program)
            change = "At line {}: nop -> jmp".format(idx)
            temp_program[idx][0] = "jmp"
        elif program[idx][0] == "jmp":
            temp_program = deepcopy(program)
            change = "At line {}: jmp -> nop".format(idx)
            temp_program[idx][0] = "nop"
        else:
            raise Exception("Unknown instruction: {}".format(program[idx][0]))
        console = Console()
        console.load_from_list(temp_program)
        console.run_no_loops()
        if console.halt:
            print("\033[92mProgram fixed!\033[0m\n" + change)
            return console


if __name__ == "__main__":
    console_1 = Console()
    console_1.load_from_file("input.txt")
    console_1.run_no_loops()
    console_2 = FixCode("input.txt")
    print("\n\n")
    print("Part 1: accumaltor before infinite loop", console_1.acc)
    print("Part 2: accumaltor after code fix", console_2.acc)
