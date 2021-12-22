import sys

class Computer:
    def __init__(self, program):
        self.program = program
        self.program_counter = 0

    def next_int(self):
        result = self.program[self.program_counter]
        self.program_counter += 1
        return result

    def run(self):
        while True:
            opcode = self.next_int()
            if opcode == 1:
                read_index_1 = self.next_int()
                read_index_2 = self.next_int()
                write_index = self.next_int()
                self.program[write_index] = self.program[read_index_1] + self.program[read_index_2]
            elif opcode == 2:
                read_index_1 = self.next_int()
                read_index_2 = self.next_int()
                write_index = self.next_int()
                self.program[write_index] = self.program[read_index_1] * self.program[read_index_2]
            elif opcode == 99:
                return
            else:
                print(f"Unknown opcode: {opcode}")
                assert False


puzzle_input = list(map(int, open(sys.argv[1]).read().split(",")))

# Part 1
part_1_program = puzzle_input.copy()
part_1_program[1] = 12
part_1_program[2] = 2

computer = Computer(part_1_program)
computer.run()
print("Part 1:", computer.program[0])


# Part 2
for noun in range(0, 100):
    for verb in range(0, 100):
        part_2_program = puzzle_input.copy()
        part_2_program[1] = noun
        part_2_program[2] = verb
        computer = Computer(part_2_program)
        computer.run()
        if computer.program[0] == 19690720:
            print("Part 2:", 100 * noun + verb)
