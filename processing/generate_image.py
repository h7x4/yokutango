#!/usr/bin/env python3

from os import scandir
from json import load
from math import floor
from PIL import Image, ImageDraw, ImageFont

width = 3000
fontsize = 60
padding = 40
spacing = 4
runspacing = 4

background_color = '#00000000'
found_color = '#A6E22E'
not_found_color = '#606060'
found_several_color = '#FF0000'
not_in_jouyou_color = '#FFFF00'

jouyou = [];
kanji = {};

for file in scandir('../kanji'):
  with open(file.path, "r") as f:
    for k in load(f):
      v = kanji.setdefault(k['kanji'], 0)
      kanji[k['kanji']] = v + 1

with open('jouyou_kanji.json', "r") as f:
  for key,value in load(f).items():
    for k in value.split():
      jouyou.append(k)

for k in kanji.keys():
  if not k in jouyou:
    kanji[k] = -1
    jouyou.append(k)

amountOfColumns = floor(width / fontsize)
amountOfRows = floor(len(jouyou) / amountOfColumns)

size = (
  width + (padding * 2) + (amountOfColumns * runspacing),
  (fontsize * amountOfRows) + (padding * 2) + (amountOfRows * spacing)
)

img = Image.new('RGBA', size, color = background_color)
fnt = ImageFont.truetype("/home/h7x4/.local/share/fonts/Sans/Droid/Droid/Droid Sans Japanese/DroidSansJapanese.ttf", fontsize)
d = ImageDraw.Draw(img)


dynamic_runspacing = (width % fontsize) / amountOfColumns
dynamic_spacing = ((len(jouyou) / amountOfColumns) % fontsize) / amountOfRows

spaceBetweenRows = (fontsize + runspacing + dynamic_runspacing)
spaceBetweenColumns = (fontsize + spacing + dynamic_spacing)

for y in range(amountOfRows):
  finished = False
  for x in range(amountOfColumns):
    k = jouyou[y * amountOfColumns + x]
    found = kanji.setdefault(k, 0)

    if found == -1:
      color = not_in_jouyou_color
    elif found == 0:
      color = not_found_color
    elif found == 1:
      color = found_color
    else:
      color = found_several_color

    text_location = (
      padding + x * spaceBetweenRows,
      padding - fontsize/2  + y * spaceBetweenColumns
    )
    d.text(text_location, k, fill= color, font=fnt)
    if (x * y == len(jouyou) - 1):
      finished = True
  if finished:
    break

# print(jouyou)
# print(kanji)

img.save('kanji.png')
