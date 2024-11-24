# File.py

import fiecommands as cmds

lowered = "Oh yes hi Fie!".casefold()
print(f"{cmds.fie_response(lowered)}\n")
print(f"{cmds.fie_response("fie")}\n")
print(f"{cmds.fie_response("fie help")}\n")

test_id1 = 420709830622183434
test_id2 = 999

print(f"{cmds.fie_time(test_id1)}\n")
print(f"{cmds.fie_time(test_id2)}\n")

op_tests = [
    "fie solve sqrt 121",
    "fie solve average 5 7 9 11",
    "fie solve 3 * 5",
    "fie solve 4 +",
    "fie solve 9 + 3 + 7",
    "fie solve 5 !"
]

for test in op_tests:
    print(f"{cmds.fie_solve(test)}\n")

days_tests = [
    "fie how many days until 06-11-2024",
    "fie how many days until",
    "fie how many days until 11-12-2024"
]

for test in days_tests:
    print(f"{cmds.fie_days_until(test)}\n")

facts_tests = [
    "fie what's zemuria",
    "fie what's zemurian ore",
    "fie what's zemurian",
    "fie what's a mecha"
]

for test in facts_tests:
    print(f"{cmds.fie_what_is(test)}\n")

