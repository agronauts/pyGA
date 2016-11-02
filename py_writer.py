from random import randint
from collections import namedtuple
from prettytable import PrettyTable
from math import floor, factorial

GENERATIONS = 500
BRANCHING_FACTOR = 2

ProgramResult = namedtuple('ProgramResult', ['program', 'output', 'compiled'])

class GAWriter(object):
    def __init__(self):
        self.char_set = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghipqrstuvwxyz!@#$%^&*()-_=+1234567890`~[]{}\:;"'
        return

    def mutate(self, orig_str):
        """Either insert or change a single character"""
        new_char = self.char_set[randint(0,len(self.char_set)-1)]
        i = randint(0,len(orig_str)-1)
        orig_str = list(orig_str)
        if randint(0,1):
            orig_str[i] = new_char
        else:
            orig_str.insert(i, new_char)
        return "".join(orig_str)

# Input
orig_prog = " "
writer = GAWriter()

# Mutation & Testing
results = [ProgramResult(orig_prog, 1, True)] #Default seed, should change
for gen in range(GENERATIONS):
    for child in range(BRANCHING_FACTOR):
        # Mutation
        parent_index = floor((len(results) - 1) / BRANCHING_FACTOR)
        mod_prog = writer.mutate(results[parent_index].program)

        # Test
        #print("** Program **")
        #print(mod_prog)
        #print("** Output **")
        try:
            res = eval(mod_prog)
        except Exception as e:
            #print("Failed to execute: ", e)
            results.append(ProgramResult(mod_prog, None, False))
        else:
            #print("It passed!")
            results.append(ProgramResult(mod_prog, res, True))

# Output
## Stats
stats_table = PrettyTable(field_names=['Stat', 'Value'])
num_compiled = len([res for res in results if res.compiled]) / len(results)
num_output = len([res for res in results if res.output]) / len(results)

stats_table.add_row(['Output', '{0:.2f}%'.format(num_output * 100)])
stats_table.add_row(['Compiled', '{0:.2f}%'.format(num_compiled * 100)])
print(stats_table)

## Compiled results
print("\n** Compiling programs **")
results_table = PrettyTable(field_names=ProgramResult._fields)
for res in [res for res in results if res.compiled]:
    results_table.add_row(res)
print(results_table)

## Leaf results
print("\n** Final generation programs **")
results_table = PrettyTable(field_names=ProgramResult._fields)
for res in results[len(results) - BRANCHING_FACTOR ** GENERATIONS:]:
    results_table.add_row(res)
print(results_table)
