#!/usr/bin/python3
import xml.etree.ElementTree as ET
import os

allbooks = ['Judges', 'Micah', 'Proverbs', 'Revelation', 'Deuteronomy', 'Haggai', '3 John', '1 Kings', 'Mark', 'Matthew', '1 Thessalonians', 'Daniel', 'Malachi', 'Colossians', 'Ruth', 'Genesis', '2 Samuel', 'Obadiah', 'Esther', 'Exodus', 'Jeremiah', 'Ephesians', 'Habakkuk', 'Luke', 'Song of Solomon', 'Jonah', 'Acts', 'Job', 'Titus', '2 Timothy', 'James', '2 John', 'Isaiah', '2 Thessalonians', '1 Chronicles', '1 Timothy', 'Leviticus', '1 Peter', 'Psalms', 'Zephaniah', 'Joel', 'Nahum', 'Jude', '2 Chronicles', 'Hosea', 'Zechariah', 'Nehemiah', 'John', '1 John', 'Lamentations', 'Amos', '1 Samuel', 'Joshua', '1 Corinthians', 'Ezra', 'Romans', '2 Corinthians', 'Hebrews', 'Ezekiel', '2 Peter', 'Philippians', 'Numbers', 'Philemon', 'Galatians', '2 Kings', 'Ecclesiastes']


class Bible:
    """
    Bible class
    """

    version = "unk"

    def __init__(self, filename):
        self.books = {}
        filename = filename.strip()

        if filename.endswith(".txt"):
            self.version = filename.split(".")[0]
        else:
            self.version = filename
            filename += ".txt"
        self.loadbible(filename)

    def get(self, bookname, c, v):
        try:
            c = int(c)
            v = int(v)
        except ValueError:
            print("Warning: chapter and verse need to be numbers!")
            return None,None
        book = self[bookname]
        if book is None:
            # check for misspellings
            mnbook = ""
            mndist = 20000 # obviously too large
            for b in allbooks:
                dst = edit_distance(b, bookname)
                if dst < mndist:
                    mnbook = b
                    mndist = dst
            r = input("Did you mean: " + mnbook + "? (Y/n)  ")
            if r in ["y", "Y", ""]:
                bookname = mnbook
                book = self[bookname]
            else:
                return None, None
        if len(book) < c:
            print("Warning: {} has only {} chapters!".format(bookname, len(book)))
            return None, None
        if len(book[c]) < v:
            print("warning: {} chapter {} has only {} verses!".format(bookname, c, len(book[c])))
            return None, None

        # return bookname also so that we can correct the loop in loadBibles
        return book[c][v], bookname 

    def __getitem__(self, n):    # if len(sys.argv) < 2:
        if n not in allbooks:
            print("Warning: You need to use the book name to reference! You said, Bible['{}'], should be " \
                  "Bible['Genesis'] (insert favorite bookname).".format(n))
            return None
        return self.books[n]

    def loadbible(self, fname):
        """
        Populates the books dict
        """
        tree = ET.parse(os.path.join("versions", fname))
        root = tree.getroot()
        for book in root.getchildren():
            bookdict = {}
            for chapter in book.getchildren():
                chapterdict = {}
                for verse in chapter.getchildren():
                    versenum = int(verse.attrib["num"])
                    chapterdict[versenum] = verse.text
                bookdict[int(chapter.attrib["num"])] = chapterdict
                
            self.books[book.attrib["name"]] = bookdict

    def __cmp__(self, other):
        return self.version.__cmp__(other.version)

