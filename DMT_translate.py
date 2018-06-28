import sys
import collections
import re
import codecs
import nltk
from nltk.util import bigrams, trigrams

def translate(): 
    spanishFile = codecs.open('SpanishText.txt', 'r','utf-8')
    translated = open('DMT_translate.txt', 'w')
    dictionary = dict()
    dictFile = codecs.open('spanishDictionary.txt', 'r','utf-8')

    for line in dictFile.readlines(): 
        print(line)
        words = line.split()
        span = words[0]
        eng = ''
        for i in range(1, len(words)): 
            eng += words[i] + ' '
        eng = eng.strip()
        dictionary[span] = eng

    for line in spanishFile.readlines(): 
        for word in line.split(): 
            w = word.lower()
            w = re.sub('[.?!",]', '', w)
            print(w)
            translated.write(dictionary[w] + ' ')
        translated.write('\n')
    return;

import nltk
import sys, re

def reorder_noun1_of_noun2(line): 
    output = []
    output.insert(0, line[len(line)-1])
    i = len(line)-2
    prev_of = (-1, -1)
    while i >= 0: 
        if i > 0: 
            previous = line[i-1]
            current = line[i]
            next = line[i+1]
            if current[0] == 'of' and check_noun_Improper(previous) and check_noun_Improper(next): 
                if prev_of[0] == -1: # no ofs in a row
                    output = output[1:]
                    output.insert(0, previous)
                    output.insert(0, next)
                    prev_of = (0, 1)
                else: 
                    output.insert(prev_of[1]+1, previous)
                    prev_of = (0, prev_of[1]+1)
                i -= 1

            else: 
                output.insert(0, current)
                prev_of = (-1, -1)
        else: 
            output.insert(0, line[i])
        i -= 1
   
    return output

def remove_be_before_verbs(line): 
    output = []
    index = 0
    while index < len(line): 
        current = line[index]
        #print 'current = ', current
        if current[0] == 'be' and index != len(line)-1: 
            next = line[index+1]
            if check_Verb(next) is False: 
                output.append(current)
        else: 
            output.append(current)
        index += 1
    return output

def check_noun_Improper(tup): 
    if tup[1] == 'NN' or tup[1] == 'NNS': 
        return True
    return False

def check_noun(tup): 
    if tup[1] == 'NN' or tup[1] == 'NNS' or tup[1] == 'NNP' or tup[1] == 'NNPS': 
        return True
    return False

def change_adjectiv_nouns(line): 
    output = line
    for i in range(1, len(output)): 
        current = output[i]
        previous = output[i-1]
        if is_adjective(current) and check_noun(previous): 
            output[i-1] = current
            output[i] = previous
    return output


def check_Verb(tup): 
    if tup[1] == 'VB' or tup[1] == 'VBD' or tup[1] == 'VBG' or tup[1] == 'VBN' or tup[1] == 'VBP' or tup[1] == 'VBZ': 
        return True
    return False

def is_adjective(tup): 
    return tup[1] == 'JJ'

def check_adverb(tup): 
    return tup[1] == 'RB'

def check_prop_noun(tup): 
    if tup[1] == 'NNP' or tup[1] == 'NNPS': 
        return True
    return False

def reorder_in_and_adverbs(line): 
    output = line
    in_index = -1
    adverbs_present = False
    in_list = []
    adverb_list = []
    i = 0
    while i < len(line):
        current = line[i]
        if current[0] == 'in': 
            in_index = i
            in_list.append(current)

        else: 
            if check_adverb(current): 
                adverb_list.append(current)
                adverbs_present = True
            else: 
                if in_index != -1 and adverbs_present is False: 
                    in_list.append(current)
                if adverbs_present is True and in_index != -1: 
                    adverbs_present = False
                    before = line[0:in_index]
                    after_index = in_index + len(in_list) + len(adverb_list)
                    after = line[after_index:]
                    line = before + adverb_list + in_list + after
                    adverb_list = []
                    in_list = []
                    in_index = -1

        i += 1

    return line

def eliminate_a_proper_noun(line): 
    output = []
    index = 1
    output.append(line[0])
    while index < len(line)-1: 
        current = line[index]
        previous = line[index-1]
        next = line[index+1]
        if current[0] == 'at': 
            if check_prop_noun(next) is False:
               
                output.append(current)
        else: 
            output.append(current)
        index += 1

    output.append(line[len(line)-1])
    return output

def remove_article_before_proper_noun(line): 
    output = []
    index = 0
    while index < len(line): 
        current = line[index]
        
        if current[1] == 'DT' and index != len(line)-1: 
            next = line[index+1]
            if check_prop_noun(next) is False: 
                output.append(current)
        else: 
            output.append(current)
        index += 1
    return output

def swap_verbs_personal_pronouns(line): 
    output = line
    for i in range(1, len(output)): 
        current = output[i]
        previous = output[i-1]
        if check_Verb(current) and previous[1] == 'PRP': 
            output[i-1] = current
            output[i] = previous
    return output

def handle_an_a(line): 
    output = line
    for i in range(0, len(output)): 
        current = output[i]
        if current[0] == 'a' and i < len(output)-1:
            next = output[i+1]
            if check_Vowel(next[0][0]): 
                output[i] = ('an', 'DT')
        if current[0] == 'an' and i < len(output)-1: 
            next = output[i+1]
            if check_Vowel(next[0][0]) is False:
                output[i] = ('a', 'DT')
    return output

def check_Vowel(ch):
    if ch == 'a' or ch == 'e' or ch == 'i' or ch == 'o' or ch == 'u': 
        return True
    return False

def eliminate_same_words(line): 
    prev_word = ''
    output = []
    output.append(line[0])
    for i in range(1, len(line)): 
        current = line[i]
        previous = line[i-1]
        if current[0] != previous[0]: 
            output.append(current)
    return output
span_eng_dict = dict()
def switch_adverbs_and_verbs(line):
    output = []
    i = 0
    while i < len(line)-1:
        currTuple = line[i]
        currWord = currTuple[0]
        if check_Verb(currTuple):
            nextTuple = line[i+1]
            nextWord = nextTuple[0]
            if check_adverb(nextTuple):
                print(currWord + ' ' + nextWord)
                output.append(nextTuple)
                output.append(currTuple)
                i += 1
            else: 
                output.append(currTuple)
        else:
            output.append(line[i])
        i += 1
    output.append(line[len(line)-1])
    return output


def swap_reflexive_verbs(line):
    output = []
    i = 0
    while i < len(line):
        currTuple = line[i]
        currWord = currTuple[0]
        if currTuple[1] == 'PRP':
            nextTuple = line[i+1]
            nextWord = nextTuple[0]
            if check_Verb(nextTuple):
                print(currWord + ' ' + nextWord)
                output.append(nextTuple)
                output.append(currTuple)
                i += 1
        else:
            output.append(line[i])
        i += 1
    return output

def check_adverb(tup):
    currWordPOS = tup[1]
    if currWordPOS == 'RB' or currWordPOS == 'RBR' or currWordPOS == 'RBS':
        return True
    return False

def create_span_eng_dictionary():
    lines = codecs.open('spanishDictionary.txt', encoding='utf-8')
    span_eng_dict = dict()
    for line in lines:
        split_words = line.split()
        spanish = split_words[0].lower()
        english = ' '.join([split_words[i].strip() for i in range(1, len(split_words))])
        #print(spanish, english)
        span_eng_dict[spanish] = english.lower()
        
    return span_eng_dict

def pos_tagging(): 
    translatedText = open('DMT_translate.txt', 'r')
    tagList = []
    for line in translatedText:
        currLine = nltk.word_tokenize(line)
        tags = nltk.pos_tag(currLine)
        print(tags)
        tagList.append(tags)


    output_file = open('DMT_output.txt', 'w')
    for line in tagList: 
        translated_text = line
        translated_text = reorder_noun1_of_noun2(translated_text)
        translated_text = remove_be_before_verbs(translated_text)
        translated_text = change_adjectiv_nouns(translated_text)
        translated_text = reorder_in_and_adverbs(translated_text)
        translated_text = eliminate_a_proper_noun(translated_text)
        translated_text = remove_article_before_proper_noun(translated_text)
        translated_text = handle_an_a(translated_text)
        translated_text = eliminate_same_words(translated_text)   
        translated_text = switch_adverbs_and_verbs(translated_text)
        translated_text = swap_reflexive_verbs(translated_text)
        for t in translated_text: 
            output_file.write(t[0] + ' ')
        output_file.write('\n')
    return;

def create_bigram_model(span_eng_dict):
    bigram_span_dict = collections.defaultdict(lambda: 0)
    bigram_eng_dict = collections.defaultdict(lambda: 0)
    bigram_span_eng_dict = collections.defaultdict(lambda: tuple)
    text = codecs.open('SpanishText.txt', encoding='utf-8')
    for sentence in text.readlines():
        line = [re.sub('[.?!",]', '', word) for word in sentence.split()]
        for word1, word2 in bigrams(line):
            bigram_span_dict[(word1.lower(), word2.lower())]+=1
        for word1, word2 in bigrams(line):
            #print(word1, span_eng_dict[word1])
            try:
                bigram_span_eng_dict[(word1.lower(), word2.lower())] = (span_eng_dict[word1.lower()], span_eng_dict[word2.lower()])
            except:
                pass    
    eng_text = open('DMT_translate.txt')
    for sentence in eng_text.readlines():
        line = [re.sub('[.?!",]', '', word) for word in sentence.split()]
        for word1, word2 in bigrams(line):
            bigram_eng_dict[(word1.lower(), word2.lower())]+=1   
    
    text = ''
    for k, v in  bigram_span_eng_dict.items():
        try:
            if (bigram_span_dict.get(k) ==   bigram_eng_dict.get(v)) and (bigram_span_dict.get(k) >=1):
                #print(k, v)
                text += k[0]+k[1]
        except:
            pass
    return;    

def create_tri_model(span_eng_dict):
    trigram_span_dict = collections.defaultdict(lambda: 0)
    trigram_eng_dict = collections.defaultdict(lambda: 0)
    trigram_span_eng_dict = collections.defaultdict(lambda: tuple)
    text = codecs.open('SpanishText.txt', encoding='utf-8')
    for sentence in text.readlines():
        line = [re.sub('[.?!",]', '', word) for word in sentence.split()]
        for word1, word2, word3 in trigrams(line):
            trigram_span_dict[(word1.lower(), word2.lower(), word3.lower())]+=1
        for word1, word2, word3 in trigrams(line):
            #print(word1, span_eng_dict[word1])
            trigram_span_eng_dict[(word1.lower(), word2.lower(), word3.lower())] = (span_eng_dict[word1.lower()], span_eng_dict[word2.lower()], span_eng_dict[word3.lower()])
    eng_text = open('DMT_output.txt')
    for sentence in eng_text.readlines():
        line = [re.sub('[.?!",]', '', word) for word in sentence.split()]
        for word1, word2, word3 in trigrams(line):
            trigram_eng_dict[(word1.lower(), word2.lower(), word3.lower())]+=1   
    text = ''
    for k, v in  trigram_span_eng_dict.items():
        try:
            if (trigram_span_dict.get(k) ==   trigram_eng_dict.get(v)) and (trigram_span_dict.get(k) >=1):
                #print(k, v)
                text += k[0]+k[1]
        except:
            pass
    return;

    
if __name__ == "__main__":
    translate()
    span_eng_dict = create_span_eng_dictionary()
    create_bigram_model(span_eng_dict)
    create_tri_model(span_eng_dict)
    pos_tagging()



