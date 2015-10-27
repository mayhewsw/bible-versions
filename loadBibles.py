#!/usr/bin/python3
import sys

import os
from bible import Bible

import pickle

bibledir = "versions/"

def picklestuff():
    #b = open("books.pkl2", "rb")
    #blist = pickle.load(b)
    #b.close()

    b = open("books.pkl", "wb")
    bdict = {}
    for bk in blist:
        bdict[bk.version] = bk

    pickle.dump(bdict, b)
    b.close()

       
if __name__ == "__main__":
    exitwords = ["q", "exit", "quit"]

    #picklestuff()

    #b = open("books.pkl", "rb")
    #bdict = pickle.load(b)
    #b.close()

    bdict = {}
    b = Bible("KJV.txt")
    bdict["KJV"] = b
    
    def chooseversion():
        while True:
            s = raw_input("Enter version: (l to list versions, can also enter comma "
                      "separated to compare, all for all versions)  ")
            if s == "l":
                print("bible version list")
                vs = os.listdir(bibledir)
                for v in vs:
                    print(v)
            else:
                if s == "all":
                    lst = bdict.keys()
                else:
                    lst = map(lambda p: p.strip(), s.split(","))
                blist = []
                for sp in lst:
                    print("loading {}".format(sp))
                    blist.append(bdict[sp])
                break

        #print("Loaded {} Bibles".format([b.version for b in blist]))
        print("Enter <book> <chap>:<verse> ")
        return blist

    blist = chooseversion()

    while True:
        s = raw_input("> ")
        if s in exitwords:
            print("Exit.")
            break
        if s == "change":
            print("Changing...")
            blist = chooseversion()
            continue
        if s == "help":
            print("Usage:\n\t<book> <chap>:<verse\n\tchange - change Bible version\n\texit, q, quit - quit")
            continue

        # Having gone past all the options, we assume
        # that s is a book chapter:verse
        sp = s.split()
        if len(sp) == 1:
            print("Normally this would print the entire book, but not now!")
            #book = sp[0]
            #for b in blist:
            #    print(b[book])
        else:
            cv = sp[-1].split(":")
            c = cv[0] # chapter
            v = cv[1] # verse
            book = " ".join(sp[:-1])
            print(book, c, v)
            for b in blist:
                val, book = b.get(book, c, v)
                if val is not None:
                    print("{}: {}".format(b.version, val))
                else:
                    break
                      

    
    


