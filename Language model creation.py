
def tokenize(all_str):
        import re
        import string
        words_all = []
        translate_table = dict((ord(char), None) for char in string.punctuation)
        for line in all_str:
            line = line.lower()
            if len(line) != 0:
                line = line.translate(translate_table)
        words_all += line
      #  words_all.append(" ")
        all_str = ''.join(words_all)
        all_str = re.sub(' +',' ',all_str)
        all_str = re.sub('\n',' ',all_str)
        all_str = re.sub(' +',' ',all_str)
        all_str = re.sub(' ',' ',all_str)
        return all_str

def char_frequency(str1):
    charfreq = {}
    for n in str1:
        keys = charfreq.keys()
        if n in keys:
            charfreq[n] += 1
        else:
            charfreq[n] = 1
    return charfreq

def word1grams(text, n=1, exact=True):
  """ Convert text into character ngrams. """
  return ["".join(j) for j in zip(*[text[i:] for i in range(n)])]

def word2grams(text, n=2, exact=True):
  """ Convert text into character ngrams. """
  return ["".join(j) for j in zip(*[text[i:] for i in range(n)])]

def word3grams(text, n=3, exact=True):
  """ Convert text into character ngrams. """
  return ["".join(j) for j in zip(*[text[i:] for i in range(n)])]

def ngramfreq(alist):
    import collections
    counter=collections.Counter(alist)
    return counter

def problem1():
    
    from nltk.corpus import udhr
    import re
    import string
    
    
    
    english = udhr.raw('English-Latin1')
    french = udhr.raw('French_Francais-Latin1')
    italian = udhr.raw('Italian_Italiano-Latin1')
    spanish = udhr.raw('Spanish_Espanol-Latin1')

    english_train, english_dev = english[0:1000], english[1000:1100]
    french_train, french_dev = french[0:1000], french[1000:1100]
    italian_train, italian_dev = italian[0:1000], italian[1000:1100]
    spanish_train, spanish_dev = spanish[0:1000], spanish[1000:1100]
    
    english_test = udhr.words('English-Latin1')[0:1000]
    french_test = udhr.words('French_Francais-Latin1')[0:1000]
    italian_test = udhr.words('Italian_Italiano-Latin1')[0:1000]
    spanish_test = udhr.words('Spanish_Espanol-Latin1')[0:1000]
    
    #english_test = english_test.split(" ")
    #spanish_test = spanish_test.split(" ")
    #italian_test = italian_test.split(" ")
    #spanish_test = spanish_test.split(" ")
    
    """Englis tain Model"""
    words_all = []
    translate_table = dict((ord(char), None) for char in string.punctuation)
    for line in english_train:
        line = line.lower()
        if len(line) != 0:
                line = line.translate(translate_table)
        words_all += line
      #  words_all.append(" ")
    all_str = ''.join(words_all)
    all_str = re.sub(' +',' ',all_str)
    all_str = re.sub('\n',' ',all_str)
    all_str = re.sub(' +',' ',all_str)
    all_str = re.sub(' ',' ',all_str)
    #print(all_str)
    onecharfreqdict = char_frequency(all_str)
    #print(onecharfreqdict)
    bilist = (word2grams(all_str))
    bicharfreqdict = ngramfreq(bilist)
    #print(bicharfreqdict)
    trilist = (word3grams(all_str))
    tricharfreqdict = ngramfreq(trilist)
    
    """French tain Model"""
    words_all = []
    translate_table = dict((ord(char), None) for char in string.punctuation)
    for line in french_train:
        line = line.lower()
        if len(line) != 0:
                line = line.translate(translate_table)
        words_all += line
    all_str = ''.join(words_all)
    all_str = re.sub(' +',' ',all_str)
    all_str = re.sub('\n',' ',all_str)
    all_str = re.sub(' +',' ',all_str)
    all_str = re.sub(' ',' ',all_str)
    print(all_str)
    french_onecharfreqdict = char_frequency(all_str)
    print(onecharfreqdict)
    bilist = (word2grams(all_str))
    french_bicharfreqdict = ngramfreq(bilist)
    print(bicharfreqdict)
    trilist = (word3grams(all_str))
    french_tricharfreqdict = ngramfreq(trilist)
   
      
    
    """English test on English vs French Unigram models:"""
    
    english_freq =0
    french_freq = 0 
    
    for i in english_test:
        #print("next word")
        i = "".join(c for c in i if c not in ('!','.',':',',',' '))
        eng_wordprob = 1
        french_wordprob = 1
        for unichar in (word1grams(i)):
            if unichar in onecharfreqdict.keys():
                eng_unicharprob = round((onecharfreqdict[unichar]/len(english_test)),4);
               # print(trichar,onecharfreqdict[trichar],unichar[0],onecharfreqdict[trichar[0]],round(eng_bicharprob,4))
                eng_wordprob *= eng_unicharprob
            if  unichar in french_onecharfreqdict.keys():
                french_unicharprob = round((french_onecharfreqdict[unichar])/len(english_test),4)
                french_wordprob *= french_unicharprob
        
        if eng_wordprob >= french_wordprob:
                english_freq +=1
        else:
               french_freq +=1
        
        print(i,round(eng_wordprob,10), round(french_wordprob,10),english_freq,french_freq)
        eng_wordprob = round(eng_wordprob,10)
        french_wordprob = round(french_wordprob,10)
        eng_unigram_probability = ((english_freq/(english_freq+french_freq)*100))
   # print(english_freq,french_freq)
    print("Accuracy of English test on English vs French Uni-gram models:  ", eng_unigram_probability,"%")        
     
    
    
    
    """English test on English vs French bigram models """
    english_freq =0
    french_freq = 0
     
    for i in english_test:
        #print("next word")
        i = "".join(c for c in i if c not in ('!','.',':',',',' '))
        eng_wordprob = 1
        french_wordprob = 1
        for bichar in (word2grams(i)):
            if bichar in bicharfreqdict.keys():
                eng_bicharprob = round(bicharfreqdict[bichar],4)/round(onecharfreqdict[bichar[0]],4);
                print(bichar,bicharfreqdict[bichar],bichar[0],onecharfreqdict[bichar[0]],round(eng_bicharprob,4))
                eng_wordprob *= eng_bicharprob
            if  bichar in french_bicharfreqdict.keys():
                french_bicharprob = round(french_bicharfreqdict[bichar],4)/round(french_onecharfreqdict[bichar[0]],4)
                french_wordprob *= french_bicharprob
        
        if eng_wordprob >= french_wordprob:
                english_freq +=1
        else:
               french_freq +=1
        
        print(i,round(eng_wordprob,10), round(french_wordprob,10),english_freq,french_freq)
        eng_wordprob = round(eng_wordprob,10)
        french_wordprob = round(french_wordprob,10)
        eng_bigram_probability = ((english_freq/(english_freq+french_freq)*100))
    #print(english_freq,french_freq)
    print("Accuracy of English test on English vs French bigram models:  ", eng_bigram_probability,"%")        
    
    
    
    """Accuracy of English test on English vs French Tri-gram models: """
    
    english_freq =0
    french_freq = 0 
    
    for i in english_test:
        #print("next word")
        i = "".join(c for c in i if c not in ('!','.',':',',',' '))
        eng_wordprob = 1
        french_wordprob = 1
        for trichar in (word3grams(i)):
            if trichar in tricharfreqdict.keys():
                eng_bicharprob = round(tricharfreqdict[trichar],4)/round(onecharfreqdict[trichar[0]],4);
                print(trichar,tricharfreqdict[trichar],trichar[0],onecharfreqdict[trichar[0]],round(eng_bicharprob,4))
                eng_wordprob *= eng_bicharprob
            if  trichar in french_tricharfreqdict.keys():
                french_bicharprob = round(french_tricharfreqdict[trichar],4)/round(french_onecharfreqdict[trichar[0]],4)
                french_wordprob *= french_bicharprob
        
        if eng_wordprob >= french_wordprob:
                english_freq +=1
        else:
               french_freq +=1
        
        print(i,round(eng_wordprob,10), round(french_wordprob,10),english_freq,french_freq)
        eng_wordprob = round(eng_wordprob,10)
        french_wordprob = round(french_wordprob,10)
        eng_trigram_probability = ((english_freq/(english_freq+french_freq)*100))
    print(english_freq,french_freq)
    print("Accuracy of English test on English vs French Tri-gram models:  ",eng_trigram_probability ,"%")        
    
    

    """ same experiment as above for Spanish vs. Italian """
    """italian_train  Model"""
    words_all = []
    translate_table = dict((ord(char), None) for char in string.punctuation)
    for line in italian_train:
        line = line.lower()
        if len(line) != 0:
                line = line.translate(translate_table)
        words_all += line
    all_str = ''.join(words_all)
    all_str = re.sub(' +',' ',all_str)
    all_str = re.sub('\n',' ',all_str)
    all_str = re.sub(' +',' ',all_str)
    all_str = re.sub(' ',' ',all_str)
    print(all_str)
    italian_onecharfreqdict = char_frequency(all_str)
    print(onecharfreqdict)
    bilist = (word2grams(all_str))
    italian_bicharfreqdict = ngramfreq(bilist)
    print(bicharfreqdict)
    trilist = (word3grams(all_str))
    italian_tricharfreqdict = ngramfreq(trilist)
    
    """spanish_train  Model"""
    words_all = []
    translate_table = dict((ord(char), None) for char in string.punctuation)
    for line in spanish_train:
        line = line.lower()
        if len(line) != 0:
                line = line.translate(translate_table)
        words_all += line
    all_str = ''.join(words_all)
    all_str = re.sub(' +',' ',all_str)
    all_str = re.sub('\n',' ',all_str)
    all_str = re.sub(' +',' ',all_str)
    all_str = re.sub(' ',' ',all_str)
    print(all_str)
    spanish_onecharfreqdict = char_frequency(all_str)
    print(onecharfreqdict)
    bilist = (word2grams(all_str))
    spanish_bicharfreqdict = ngramfreq(bilist)
    print(bicharfreqdict)
    trilist = (word3grams(all_str))
    spanish_tricharfreqdict = ngramfreq(trilist)
    

    """spanish test on Spanish vs Italian Unigram models:"""
    
    spanish_freq =0
    italian_freq = 0 
    
    for i in spanish_test:
        #print("next word")
        i = "".join(c for c in i if c not in ('!','.',':',',',' '))
        spanish_wordprob = 1
        italian_wordprob = 1
        for unichar in (word1grams(i)):
            if unichar in spanish_onecharfreqdict.keys():
                spanish_unicharprob = round((spanish_onecharfreqdict[unichar]/1000),4);
               # print(trichar,spanish_onecharfreqdict[trichar],unichar[0],spanish_onecharfreqdict[trichar[0]],round(eng_bicharprob,4))
                spanish_wordprob *= spanish_unicharprob
            if  unichar in italian_onecharfreqdict.keys():
                italian_unicharprob = round((italian_onecharfreqdict[unichar])/1000,4)
                italian_wordprob *= italian_unicharprob
        
        if spanish_wordprob >= italian_wordprob:
                spanish_freq +=1
        else:
               italian_freq +=1
        
        #print(i,round(spanish_wordprob,10), round(italian_wordprob,10),spanish_freq,italian_freq)
        spanish_wordprob = round(spanish_wordprob,10)
        italian_wordprob = round(italian_wordprob,10)
        spanish_unigram_probability = ((spanish_freq/(spanish_freq+italian_freq)*100))
    #print("Accuracy of Spanish test on Spanish vs Italian Uni-gram models:  ", spanish_unigram_probability,"%")        
    
    
    """spanish test on Spanish vs Italian Bi-gram models:"""
    
    spanish_freq =0
    italian_freq = 0 
    
    for i in spanish_test:
        #print("next word")
        i = "".join(c for c in i if c not in ('!','.',':',',',' '))
        spanish_wordprob = 1
        italian_wordprob = 1
        for bichar in (word2grams(i)):
            if bichar in spanish_bicharfreqdict.keys():
                spanish_bicharprob = round(spanish_bicharfreqdict[bichar],4)/round(spanish_onecharfreqdict[bichar[0]],4);
               # print(trichar,spanish_onecharfreqdict[trichar],bichar[0],spanish_onecharfreqdict[trichar[0]],round(eng_bicharprob,4))
                spanish_wordprob *= spanish_bicharprob
            if  bichar in italian_bicharfreqdict.keys():
                italian_bicharprob = round(italian_bicharfreqdict[bichar],4)/round(italian_onecharfreqdict[bichar[0]],4);
                italian_wordprob *= italian_bicharprob
        
        if spanish_wordprob > italian_wordprob:
                spanish_freq +=1
        else:
               italian_freq +=1
        
        #print(i,round(spanish_wordprob,10), round(italian_wordprob,10),spanish_freq,italian_freq)
        spanish_wordprob = round(spanish_wordprob,10)
        italian_wordprob = round(italian_wordprob,10)
        spanish_bigram_probability = ((spanish_freq/(spanish_freq+italian_freq)*100))
    #print("Accuracy of Spanish test on Spanish vs Italian bi-gram models:  ", spanish_bigram_probability,"%")        
     
    
    """spanish test on Spanish vs Italian Tri-gram models:"""
    
    spanish_freq =0
    italian_freq = 0 
    
    for i in spanish_test:
        #print("next word")
        i = "".join(c for c in i if c not in ('!','.',':',',',' '))
        spanish_wordprob = 1
        italian_wordprob = 1
        for bichar in (word3grams(i)):
            if bichar in spanish_tricharfreqdict.keys():
                spanish_bicharprob = round(spanish_tricharfreqdict[bichar],4)/round(spanish_onecharfreqdict[bichar[0]],4);
                print(bichar,spanish_tricharfreqdict[bichar],bichar[0],spanish_onecharfreqdict[trichar[0]],(spanish_bicharprob))
                spanish_wordprob *= spanish_bicharprob
            if  bichar in italian_tricharfreqdict.keys():
                italian_bicharprob = round(italian_tricharfreqdict[bichar],4)/round(italian_onecharfreqdict[bichar[0]],4);
                italian_wordprob *= italian_bicharprob
        
        if spanish_wordprob >= italian_wordprob:
                spanish_freq +=1
        else:
               italian_freq +=1
        
        #print(i,round(spanish_wordprob,10), round(italian_wordprob,10),spanish_freq,italian_freq)
        spanish_wordprob = round(spanish_wordprob,10)
        italian_wordprob = round(italian_wordprob,10)
        spanish_trigram_probability = ((spanish_freq/(spanish_freq+italian_freq)*100))
    #print("Accuracy of Spanish test on Spanish vs Italian tri-gram models:  ", spanish_trigram_probability,"%")      
    
    print("Accuracy of English test on English vs French Uni-gram models:  ", eng_unigram_probability,"%") 
    print("Accuracy of English test on English vs French bigram models:  ", eng_bigram_probability,"%") 
    print("Accuracy of English test on English vs French Tri-gram models:  ",eng_trigram_probability ,"%")
    print("\nAccuracy of Spanish test on Spanish vs Italian Uni-gram models:  ", spanish_unigram_probability,"%")
    print("Accuracy of Spanish test on Spanish vs Italian bi-gram models:  ", spanish_bigram_probability,"%")   
    print("Accuracy of Spanish test on Spanish vs Italian tri-gram models:  ", spanish_trigram_probability,"%")
    

    return 

    



    



problem1()  