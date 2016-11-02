from random import randint
from collections import namedtuple
from prettytable import PrettyTable

ITERATIONS = 100

ProgramResult = namedtuple('ProgramResult', ['program', 'output', 'compiled'])

class GAWriter(object):
    def __init__(self):
        self.char_set = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghipqrstuvwxyz!@#$%^&*()-_=+1234567890`~[]{}\:;"'
        return

    def mutate(self, orig_str):
        """Perform a single mutation"""
        new_char = self.char_set[randint(0,len(self.char_set)-1)]
        i = randint(0,len(orig_str)-1)
        orig_str = list(orig_str)
        orig_str[i] = new_char
        return "".join(orig_str)

# Input
orig_prog = "5 + 5 * 2 + 3"
writer = GAWriter()

results = []
for i in range(ITERATIONS):
    # Mutation
    mod_prog = writer.mutate(orig_prog)

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
print("\n** Results **")
table = PrettyTable(field_names=ProgramResult._fields)
for res in results:
    table.add_row(res)
print(table)
