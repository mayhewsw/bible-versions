#!/usr/bin/ipython
from bs4 import *
import urllib
import sys
import codecs
import collections
import operator

searchurl = "http://www.biblegateway.com/passage/?search={0}+{1}&version={2}"

books = [("Genesis", 50),
         ("Exodus",40),
         ("Leviticus",27),
         ("Numbers",36),
         ("Deuteronomy",34),
         ("Joshua", 24),
         ("Judges", 21),
         ("Ruth",4),
         ("1 Samuel",31),
         ("2 Samuel", 24),
         ("1 Kings", 22),
         ("2 Kings", 25),
         ("1 Chronicles", 29),
         ("2 Chronicles",36),
         ("Ezra", 10),
         ("Nehemiah", 13),
         ("Esther", 10),
         ("Job", 42),
         ("Psalms", 150),
         ("Proverbs",31),
         ("Ecclesiastes",12),
         ("Song of Solomon",8),
         ("Isaiah",66),
         ("Jeremiah",52),
         ("Lamentations",5),
         ("Ezekiel",48),
         ("Daniel",12),
         ("Hosea",14),
         ("Joel",3),
         ("Amos",9),
         ("Obadiah",1),
         ("Jonah",4),
         ("Micah",7),
         ("Nahum",3),
         ("Habakkuk",3),
         ("Zephaniah",3),
         ("Haggai",2),
         ("Zechariah",14),
         ("Malachi",4),
         ("Matthew",28),
         ("Mark",16),
         ("Luke",24),
         ("John",21),
         ("Acts",28),
         ("Romans",16),
         ("1 Corinthians",16),
         ("2 Corinthians",13),
         ("Galatians",6),
         ("Ephesians",6),
         ("Philippians",4),
         ("Colossians",4),
         ("1 Thessalonians",5),
         ("2 Thessalonians",3),
         ("1 Timothy",6),
         ("2 Timothy",4),
         ("Titus",3),
         ("Philemon",1),
         ("Hebrews",13),
         ("James",5),
         ("1 Peter",5),
         ("2 Peter",3),
         ("1 John",5),
         ("2 John",1),
         ("3 John",1),
         ("Jude",1),
         ("Revelation", 22)]

def spacereplacer(exc):
    return u" ", exc.end
codecs.register_error("spacereplace", spacereplacer)

def getChap(book, chapnum, version, out=sys.stdout):
    out.write("<chapter num=\"{0}\">\n".format(chapnum))
    
    f = urllib.urlopen(searchurl.format(book, chapnum, version))
    html = f.read()
    soup = BeautifulSoup(html)
    
    cont = soup.find("div", {"class": "passage"})
    verses = cont.findAll("span", {"class": "text"})

    outverses = collections.defaultdict(str)
    
    #out.write("book: {0}, chapter: {1}, version: {2}".format(book, chapnum, version) + "\n")
    first = True
    for verse in verses:
        
        classes = verse.get("class")
        verseinfo = classes[-1]
        versenum = int(verseinfo.split("-")[-1])
        
        # this is to avoid section headings
        if verse.parent.name == "h3":
            continue
        versetokens = verse.text.encode("ascii", "spacereplace").split()
        # usually we remove the first token because it is the versenum
        # this is not true for all verses (eg poetry)
        try:
            int(versetokens[0])
            versetext = " ".join(versetokens[1:])
        except ValueError:
            versetext = " ".join(versetokens)
        except IndexError:
            continue
        
        outverses[versenum] += " " + versetext


    sorted_verses = sorted(outverses.iteritems(), key=operator.itemgetter(0))
    #for versenum in outverses:
    for versenum, versetext in sorted_verses:
        #versetext = outverses[versenum].strip()
        out.write("<verse num=\"{0}\">{1}</verse>\n".format(versenum, versetext.strip()))
    
    out.write("</chapter>\n")


versions = {"KJ21" : "21st Century King James Version",
"ASV" : "American Standard Version",
"AMP" : "Amplified Bible",
"CEB" : "Common English Bible",
"CJB" : "Complete Jewish Bible",
"CEV" : "Contemporary English Version",
"DARBY" : "Darby Translation",
"DRA" : "Douay-Rheims 1899 American Edition",
"ERV" : "Easy-to-Read Version",
"ESV" : "English Standard Version",
"ESVUK" : "English Standard Version Anglicised",
"EXB" : "Expanded Bible",
"GNV" : "1599 Geneva Bible",
"GW" : "GOD'S WORD Translation",
"GNT" : "Good News Translation",
"HCSB" : "Holman Christian Standard Bible",
"PHILLIPS" : "J.B. Phillips New Testament",
"KJV": "King James Version",
"AKJV" : "Authorized (King James) Version",
"KNOX" : "Knox Bible",
"LEB" : "Lexham English Bible",
"MSG" : "The Message",
"MOUNCE" : "Mounce Reverse-Interlinear New Testament",
"NOG" : "Names of God Bible",
"NASB" : "New American Standard Bible",
"NCV" : "New Century Version",
"NET" : "New English Translation (NET Bible)",
"NIRV" : "New International Readers Version",
"NIV" : "New International Version",
"NIVUK" : "New International Version - UK",
"NKJV" : "New King James Version",
"NLV" : "New Life Version",
"NLT" : "New Living Translation",
"NRSV" : "New Revised Standard Version",
"NRSVA" : "New Revised Standard Version, Anglicised",
"NRSVACE" : "New Revised Standard Version Anglicised Catholic Edition",
"NRSVCE" : "New Revised Standard Version Catholic Edition",
"OJB" : "Orthodox Jewish Bible",
"RSV" : "Revised Standard Version",
"RSVCE" : "Revised Standard Version Catholic Edition",
"VOICE" : "The Voice",
"WEB" : "World English Bible",
"WE" : "Worldwide English (New Testament)",
"WYC" : "Wycliffe Bible",
"YLT" : "Young's Literal Translation"}

for version in versions:
    print "Getting version: {0}".format(version)
    fname = "{0}.txt".format(version)
    try:
        open(fname)
        print "Oh, {0} is already there".format(fname)
        continue        
    except IOError:
        pass
    out = open(fname, "w")
    out.write("<bible>\n")
    try:
        for book in books:
            print "Getting book: {0}".format(book)
            out.write("<book name=\"{0}\">\n".format(book[0]))
            for chap in range(1, book[1]+1):
                print "Getting chapter: {0}".format(chap)
                getChap(book[0], str(chap), version, out)
            out.write("</book>\n")
    except AttributeError as e:
        print e
        print "moving on"
            
    out.write("</bible>")
    out.close()






