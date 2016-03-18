# -*- coding: utf-8 -*-
# Wordnet via Python3
# 
# ref:
#   WordList_JP: http://compling.hss.ntu.edu.sg/wnja/
#   python3: http://sucrose.hatenablog.com/entry/20120305/p1
import sys, sqlite3,random
from collections import namedtuple
from pprint import pprint

conn = sqlite3.connect("./wnjpn.db")

Word = namedtuple('Word', 'wordid lang lemma pron pos')

def getWords(lemma):
  cur = conn.execute("select * from word where lemma=?", (lemma,))
  return [Word(*row) for row in cur]

 
Sense = namedtuple('Sense', 'synset wordid lang rank lexid freq src')

def getSenses(word):
  cur = conn.execute("select * from sense where wordid=?", (word.wordid,))
  return [Sense(*row) for row in cur]

Synset = namedtuple('Synset', 'synset pos name src')

def getSynset(synset):
  cur = conn.execute("select * from synset where synset=?", (synset,))
  return Synset(*cur.fetchone())

def getWordsFromSynset(synset, lang):
  cur = conn.execute("select word.* from sense, word where synset=? and word.lang=? and sense.wordid = word.wordid;", (synset,lang))
  return [Word(*row) for row in cur]

def getWordsFromSenses(sense, lang="jpn"):
  synonym = {}
  for s in sense:
    lemmas = []
    syns = getWordsFromSynset(s.synset, lang)
    for sy in syns:
      lemmas.append(sy.lemma)
    synonym[getSynset(s.synset).name] = lemmas
  return synonym

def getSynonym (word):
    synonym = {}
    words = getWords(word)
    if words:
        for w in words:
            sense = getSenses(w)
            s = getWordsFromSenses(sense)
            synonym = dict(list(synonym.items()) + list(s.items()))
    return synonym


if __name__ == '__main__':
  if len(sys.argv) >= 2:
    good_words=[]
    bad_words=[]
    good_tag_list=["not_bad","great","marvellous","phenomenal","tip-top"]
    bad_tag_list=["worried","anxiety","concerned","fear","anxiety"]
    synonym = getSynonym(sys.argv[1])
#    print(synonym.keys())
#    pprint(synonym)
    for j in good_tag_list:
      if j in synonym.keys():
        for i in synonym[j]:
          if i not in good_words:
            good_words.append(i)
    if good_words:
      for gw in good_words:
        print("あなたは%sです"%gw)
    for k in bad_tag_list:
      if k in synonym.keys():
        for l in synonym[k]:
          if l not in bad_words:
            bad_words.append(l)
    if bad_words:
      for bw in bad_words:
        print("あなたのことが%sです"%bw)
  else:
    print("You need at least 1 argument as a word like below.\nExample:\n  $ python3 wordnet_jp 楽しい")
