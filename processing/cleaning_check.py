#!/usr/bin/env python3

from os import scandir
from json import load
import re

han = re.compile(u'.*[⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎].*', re.UNICODE)

kanji = {};

for file in scandir('../kanji'):
  with open(file.path, "r") as f:
    for k in load(f):
      kanji[k['kanji']] = k

print('More/less than one character in "kanji" field:')
for k in kanji.keys():
  if len(k) != 1:
    print(k)
print()

print('Kanji in "active" field:')
for k in kanji.values():
  for word in k['kana']:
    if type(word) is list:
      if any(han.match(piece['text']) and piece.setdefault('active', False) == True for piece in word):
        print(k)
print()

def allUnique(x):
  seen = []
  return not any(i in seen or seen.append(i) for i in x)

print('Duplicate kana fields:')
for k in kanji.values():
  if not allUnique(k['kana']):
    print(k)
print()

print('Missing "active" fields:')
for k in kanji.values():
  for word in k['kana']:
    if type(word) is list:
      if not any(piece.setdefault('active', False) == True for piece in word):
        print(k)
