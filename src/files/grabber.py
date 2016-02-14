"""
Jason Brooks
jayhaceo@gmail.com
@jaythaceo
"""

wordsFile = open('words2.txt')
for line in wordsFile:
  line = line.rstrip()
  newLine = line.upper()
  print newLine
