
text = "X-DSPAM-Confidence:    0.8475";
finder = '0.8475'
newNumber = text.find(finder)
finalNumber = text[23:]
newNumber = float(finalNumber)
print(newNumber)
