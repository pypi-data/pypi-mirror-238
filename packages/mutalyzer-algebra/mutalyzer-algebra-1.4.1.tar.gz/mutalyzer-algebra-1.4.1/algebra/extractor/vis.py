from cover import find_pmrs, inv_array
from words import nth_fibonacci_word
import os
import subprocess


def find_pmrs2(word):
    with open("/tmp/word.txt", "w") as fd:
        fd.write(word)
    os.system("../../../repeats/mreps/mreps -allowsmall /tmp/word.txt > /tmp/pmrs.txt")
    with open("/tmp/pmrs.txt") as fd:
        return eval(fd.read())


for i in range(1, 40):
    word = nth_fibonacci_word(i)
    n = len(word)
    pmrs = find_pmrs2(word)
    inv = inv_array(n, pmrs)
    print(n, len(pmrs), max([len(x) for x in inv], default=0), sum([len(x) for x in inv]))
