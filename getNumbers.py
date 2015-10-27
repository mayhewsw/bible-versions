#!/usr/bin/python
import os
from bible import Bible

import pickle
import re

from collections import defaultdict

def func():
    b = Bible("ESV")

    pat = re.compile(r"\d+,?\d+")
    
    verse, bkname = b.get("Psalms", "1", "1")
    print verse
    print bkname

    nums = defaultdict(int)

    for k in b.books.keys():
        for c in b.books[k].keys():
            for v in b.books[k][c].keys():
                versetext = b.books[k][c][v]
                groups = re.findall(pat, versetext)
                if len(groups) > 0:
                    print groups, versetext
                    for g in groups:
                        nums[g[0]] += 1

    print nums

    import matplotlib.pyplot as plt
    from numpy.random import normal
    gaussian_numbers = normal(size=10)

    print gaussian_numbers

    ln = nums.items()
    sln = sorted(ln)
    print sln
    sln = sln[1:]
    plt.bar(map(int, map(lambda p: p[0], sln)), map(lambda p: p[1], sln))
    plt.title("Benford's Law in Bible Numbers")
    plt.xlabel("Initial Digit")
    plt.ylabel("Count")
    plt.show()

if __name__ == "__main__":
    func()
