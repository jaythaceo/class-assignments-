"""
Read through the text find the
average of all integer values.
"""
count = 0
mbox = "mbox-short.txt"
fh = open(mbox)
for line in fh:
  if not line.startswith("X-DSPAM-Confidence:") : continue
  line = line[19:]
  count =  count + 1
  numbers =  float(line) / count
print numbers

def test(h):
    """something test"""
    h = "hello"
    return h
