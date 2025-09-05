

from itertools import permutations

name = 'cemil'
surname = 'tagiyev'
age = "2007"
extras = [".","!","@","#","123"]

elements = [name,surname,age]

with open("/home/samurai/Desktop/Python_For_Hacking/wordlist.txt","w") as f:

    for i in range(2,4):
        for combo in permutations(elements,i):
            base = "".join(combo)

            for extra in extras:
                f.write(base + extra + "\n")

