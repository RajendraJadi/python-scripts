from collections import *
import math
import sys
import codecs

frenchfile = "fr-en\\dev\\newstest2012.fr"
engfile = "fr-en\\dev\\newstest2012.en"
trans = "IBM_translation.txt"
outFile = "IBM1_output.txt"

def readfile(filePath, source):
    f = codecs.open(filePath,"r+",encoding="utf-8")
    text = f.read()
    data = text.split("\n")
    sents = {}    
    count = 0
    for sent in data:
        if sent != "":
            if source:
                sent = "NULL " + sent
            sents[count] = sent
            count=count+1
    f.close()
    return sents

engHash = readfile(engfile, False)
frHash = readfile(frenchfile, True)
numSents = len(engHash.keys())
pEgivenG = {}
sentMap = {}

for i in range(0, numSents):
    sentMap[frHash[i]] = engHash[i]


wordFtoWordE = {}
with codecs.open(trans,encoding="utf-8") as f:
    content = f.readlines()

for wordPair in content:
    words = wordPair.split(" ")
    pair = (words[1], words[0])
    wordFtoWordE[pair] = float(words[2])

align = ""


file = codecs.open(outFile, 'w',encoding='utf-8')
for i in range(0, numSents):
    sent = frHash[i]
    wordsF =sent.split(" ")
    eng = sentMap[sent]
    wordsE = eng.split(" ")
    engtext = ""
    frtext = ""

    for wordE in wordsE:
        keys = [(wordE,x) for x in wordsF]
        max = 0 
        w = ""
        for key in keys:
            if key in wordFtoWordE.keys():            
                if float(wordFtoWordE[key])>max:
                    max = float(wordFtoWordE[key])
                    w = key[0]
                    f = key[1]
        if w == "": 
            engtext += wordE + " "   
            align += str(0) + " "
            frtext += "NULL" + " "
        elif f == "NULL":
            engtext += wordE + " "   
            align += str(0) + " "
            frtext += "NULL" + " "
#         else:    
#             engtext += w + " "   
#             align += str(wordsF.index(f)) + " " 
#             frtext += f + " "
    frtext +="\n"
    engtext +="\n"
    align +="\n"
    #print(engtext)
    #file.write(frtext)
    #print(align)
    #print
    file.write(engtext)
    
    

#f = open(outFile, 'w')
#file.write(align)
#file.write(engtext)
file.close()





    
