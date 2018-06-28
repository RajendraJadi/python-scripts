# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 11:44:39 2017

@author: Admin
"""


def splitString(funny):
    a,b,c,d,e = funny.split(" ")
    print(a)
    print(b)
    print(c)
    print(d)
    print(e)
    return;

def secondLetter(funny):
    a,b,c,d,e = funny.split(" ")
    print(a[1]+b[1]+c[1]+d[1]+e[1])
    return;

def noSleep(phrases):
    print("List without sleep",phrases[:-1])
    return;

def joinWords(phrases):
    phrases = " ".join(phrases)
    print(phrases)
    return

def alphabeticalOrder(funny):
    alist = funny.split(" ")
    alist.sort()
    print("\n".join(alist))
    return;

def problem2(aString):
    alist = aString.split(" ")
    alist.sort()
    #unique_words = []
    frequency = {}
    for word in alist:
        count = frequency.get(word,0)
        frequency[word] = count + 1
     
    frequency_list = frequency.keys()

    for words in frequency_list:
        print (words, frequency[words])
    return;
   

import re
def problem4():
    str = " austen-emma.txt:hart@vmd.cso.uiuc.edu (internet) hart@uiucvmd (bitnet)  austen-emma.txt:Internet (72600.2026@compuserve.com); TEL: (212-254-5093) .austen-persuasion.txt:Editing by Martin Ward (Martin.Ward@uk.ac.durham)  blake-songs.txt:Prepared by David Price, email ccx074@coventry.ac.uk "
    match = re.findall(r'[\w\.-]+@[\w\.-]+', str)
    print(match)
    return

def problem5():
    print("*******Input file with duplicate lines*******")
    document_text = open('prob5.txt', 'r')
    text_string = document_text.read().lower()
    print(text_string)


    lines = []
    outfile = open('newfile.txt', 'w')
    for line in open('prob5.txt', 'r'):
        if line not in lines:
            lines.append(line)
            outfile.write(line)
    outfile.close()
    print("*******Output file after removing duplicate lines*******")
    document_text = open('newfile.txt', 'r')
    text_string = document_text.read().lower()
    print(text_string)
    return
    
from nltk.stem.porter import PorterStemmer
#from nltk.tokenize import sent_tokenize, word_tokenize

def problem7_d():
    stem_words =[]
    document_text = open('positive.txt', 'r')
    text_string = document_text.readlines()
    #print(text_string)
   # text_string.split(" ")
    ps = PorterStemmer()
    #words = word_tokenize(text_string)
    #print("Stem %s: %s" % ("studying", ps.stem("studying")))
    for line in text_string:
        stem_words.append(ps.stem(line.lower().strip()))
        #print("Stem %s: %s" % (line, ps.stem(line.lower().strip())))
    print(stem_words)
import re
import string

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.porter import PorterStemmer
from nltk.stem.lancaster import LancasterStemmer
from nltk.tokenize import RegexpTokenizer
from collections import Counter


def problem7a():
    document_text = open('debate.txt', 'r')
    text = document_text.readlines()
    text = ''.join(text)
    text =re.sub("[\(\[].*?[\)\]]", "", text)
    LEHRER = ''.join(re.findall("""LEHRER: (.+)""", text))
    OBAMA = ''.join(re.findall("""OBAMA: (.+)""", text))
    ROMNEY = ''.join(re.findall("""ROMNEY: (.+)""", text))
    
    
    print("\n\nStatements made by LEHRER: \n\n"+LEHRER)
    print("\n\nStatements made by OBAMA: \n\n"+OBAMA)
    print("\n\nStatements made by ROMNEY: \n\n"+ROMNEY)
    return{'LEHRER':LEHRER,'OBAMA':OBAMA,'ROMNEY':ROMNEY};

def problem7b(debate):
    porterStemmer = PorterStemmer()
    snowballStemmer = SnowballStemmer("english", ignore_stopwords=False)
    lancasterStemmer = LancasterStemmer()
   # cachedStopWords = stopwords.words("english")
    tokenizer = RegexpTokenizer(r'\w+')
    stemDict = {'LEHRER': {},'OBAMA': {}, 'ROMNEY': {}}
    
    LEHRER = debate['LEHRER']
    OBAMA = debate['OBAMA']
    ROMNEY = debate['ROMNEY']
    
    LEHRER = "".join(LEHRER)
    LEHRER = tokenizer.tokenize(LEHRER)
    LEHRER = ' '.join([word.lower() for word in LEHRER if word not in stopwords.words("english")])
    
    pstemmed_words = ' '.join([porterStemmer.stem(word) for word in LEHRER.split(' ')])
    stemDict['LEHRER'].update({'porterStemmer':pstemmed_words})
    stemDict11 = stemDict['LEHRER']['porterStemmer']
    print("\n\n\nLEHRER:porterStemmer\n\n ",stemDict11)
    
    sstemmed_words = ' '.join([snowballStemmer.stem(word) for word in LEHRER.split(' ')])
    stemDict['LEHRER'].update({'snowballStemmer':sstemmed_words})
    stemDict12 = stemDict['LEHRER']['porterStemmer']
    print("\n\n\nLEHRER:snowballStemmer \n\n ",stemDict12)
    
    lstemmed_words = ' '.join([lancasterStemmer.stem(word) for word in LEHRER.split(' ')])
    stemDict['LEHRER'].update({'lancasterStemmer':lstemmed_words})
    stemDict13 = stemDict['LEHRER']['lancasterStemmer']
    print("\n\n\nLEHRER:lancasterStemmer \n\n ",stemDict13)
    
    
    
    OBAMA = "".join(OBAMA)
    OBAMA = tokenizer.tokenize(OBAMA)
    OBAMA = ' '.join([word.lower() for word in OBAMA if word not in stopwords.words("english")])
    
    pstemmed_words = ' '.join([porterStemmer.stem(word) for word in OBAMA.split(' ')])
    stemDict['OBAMA'].update({'porterStemmer':pstemmed_words})
    stemDict21 = stemDict['OBAMA']['porterStemmer']
    print("\n\n\nOBAMA:porterStemmer\n\n ",stemDict21)
	
    sstemmed_words = ' '.join([snowballStemmer.stem(word) for word in OBAMA.split(' ')])
    stemDict['OBAMA'].update({'snowballStemmer':sstemmed_words})
    stemDict22 = stemDict['OBAMA']['porterStemmer']
    print("\n\n\nOBAMA:snowballStemmer \n\n ",stemDict22)
	
    lstemmed_words = ' '.join([lancasterStemmer.stem(word) for word in OBAMA.split(' ')])
    stemDict['OBAMA'].update({'lancasterStemmer':lstemmed_words})
    stemDict23 = stemDict['OBAMA']['lancasterStemmer']
    print("\n\n\nOBAMA:lancasterStemmer \n\n ",stemDict23)
    
    
    ROMNEY = "".join(ROMNEY)
    ROMNEY = tokenizer.tokenize(ROMNEY)
    ROMNEY = ' '.join([word.lower() for word in ROMNEY if word not in stopwords.words("english")])
    
    pstemmed_words = ' '.join([porterStemmer.stem(word) for word in ROMNEY.split(' ')])
    stemDict['ROMNEY'].update({'porterStemmer':pstemmed_words})
    stemDict31 = stemDict['ROMNEY']['porterStemmer']
    print("\n\n\nROMNEY:porterStemmer\n\n ",stemDict31)
	
    sstemmed_words = ' '.join([snowballStemmer.stem(word) for word in ROMNEY.split(' ')])
    stemDict['ROMNEY'].update({'snowballStemmer':sstemmed_words})
    stemDict32 = stemDict['ROMNEY']['porterStemmer']
    print("\n\n\nROMNEY:snowballStemmer \n\n ",stemDict32)
	
    lstemmed_words = ' '.join([lancasterStemmer.stem(word) for word in ROMNEY.split(' ')])
    stemDict['ROMNEY'].update({'lancasterStemmer':lstemmed_words})
    stemDict33 = stemDict['ROMNEY']['lancasterStemmer']
    print("\n\n\nROMNEY:lancasterStemmer \n\n ",stemDict33)
    
    return stemDict#{stemDict['LEHRER']['porterStemmer']:stemDict11, stemDict['OBAMA']['porterStemmer']:stemDict21 ,stemDict['ROMNEY']['porterStemmer']:stemDict31};


def problem7c(stemDict):
        stemDict11 = stemDict['LEHRER']['porterStemmer']
        #stemDict22 = stemDict['OBAMA']['porterStemmer']
        #stemDict31 = stemDict['ROMNEY']['porterStemmer']
        words = re.findall(r'\w+', stemDict11)
        """
        LEHRERlist = stemDict11.split(" ")
        frequency = {}
        for word in LEHRERlist:
                count = frequency.get(word,0)
                frequency[word] = count + 1
     
        frequency_LEHRERlist = frequency.keys()
        """
        print(Counter(words).most_common(10))
        
        """
        for words in frequency_LEHRERlist:
            print (words, frequency[words])
        """ 
                
        return

def problem7e(stemDict):
    maximum = {}
    with open('positive.txt', 'r+') as p:
        positive_text = p.readlines()
    positive_text = [word.strip() for word in positive_text]
    #print(positive_text)
    for key , value in stemDict.items():
        text = stemDict[key]['porterStemmer'].split(' ')
        #print(len(text))
        x = [word for word in text if word in positive_text]
        print('this is list...........................................\n\n\n\n')
        for word in x:
            #print('this is list...........................................\n\n\n\n')
            print(word)
        maximum['{0}'.format(key)] = len(x)
        print('i am', key)
        print(Counter(x).most_common(10))
    print('\nThe speaker uses the positive words listed in the positive word dictionary most often is :',max(maximum))


   

funny = "colorless green ideas sleep furiously"
splitString(funny)
secondLetter(funny)
phrases = funny.split(" ")
noSleep(phrases)
joinWords(phrases)
alphabeticalOrder(funny)

aString = "colorless colorless zebra green ideas ideas"
problem2(aString)

problem4()
problem5()


debate = problem7a()
stemDict = problem7b(debate)
problem7c(stemDict)
problem7_d()
problem7e(stemDict)

