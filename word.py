fname = raw_input("Enter file name: ")
fh = open(fname)
numberOfLines = 0

for line in fh:
  numberOfLines = numberOfLines + 1
print "Line count: ", numberOfLines
