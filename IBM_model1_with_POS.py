from __future__ import division
import numpy as np

from math import log
import codecs
import sys
from collections import Counter
import collections


CUT_OFF = 10**(-5)
MAX = 30
french_file = "fr-en\\train\\europarl-v7.fr-en.fr"
english_file = "fr-en\\train\\europarl-v7.fr-en.en"
translated_output = "IBM_translation_pos.txt"
french_dev_file = "fr-en\\dev\\newstest2012.fr"

pairs = [] 
def generate_english_vocab(english_file):
    """
    Takes english file as input and generates list of string of sentences
    """
    english_dict = {}
    eng_count = 0    
    with codecs.open(english_file, encoding='utf-8') as english_file:
        for sentence in english_file:
            eng_split_sent = sentence.lower().split()
            pairs.append([eng_split_sent])           
            for word in eng_split_sent:
                if word not in english_dict:
                    english_dict[word] = eng_count
                    eng_count += 1
    return english_dict, eng_count

def generate_french_vocab(french_file):
    """
    Takes french corpus file as input and generates list of string of sentences.
    """  
    span_count = 0       
    span_dict = {} 
    count = 0 

    with codecs.open(french_file, encoding='utf-8') as french_file:
        for sentence in french_file:
            span_split_sent = sentence.lower().split()
            span_split_sent.append("null")
            pairs[count].append(span_split_sent)
            count += 1     
            for word in span_split_sent:
                if word not in span_dict:
                    span_dict[word] = span_count
                    span_count += 1
    return span_dict, count, span_count

def init_translation_table(span_count, eng_count):
    """
    Develop initial translation table 
    """
    return np.ones([span_count, eng_count]) / eng_count

def populate_translation_table(english_dict,eng_count,span_dict, count, span_count,translation_table):

    loop_count = 0
    ol = -2 # dummy values
    nl = -1   
    while loop_count < 2 or abs(nl - ol) > CUT_OFF:    
    
            loop_count += 1        
            if loop_count > 1: 
                ol = nl
            if loop_count > MAX: 
                break   
            nl = 0
            count_eng_span = np.zeros([span_count, eng_count]) #init to all zeros
            #print(count_e_f)
            total_span = np.zeros(span_count)        
            for pair in pairs:              
                english_index = Counter([english_dict[p] for p in pair[0]])   
                #print(indeng)         
                span_index  = Counter([span_dict[p] for p in pair[1]])                        
                eng_sorted = sorted(english_index)
                span_sorted = sorted(span_index)
                indexes = np.ix_(span_sorted, eng_sorted)
                weighted_translation = translation_table[indexes]    
                for index, pos in enumerate(eng_sorted): 
                    #print(index)
                    if english_index[pos] > 1: weighted_translation[:, index] *= english_index[pos]           
    
                for index, pos in enumerate(span_sorted): 
                    if span_index[pos] > 1:  weighted_translation[index, :] *= span_index[pos]                              
                sum = np.sum(weighted_translation, axis=0)            
                nl += np.sum(np.log(sum))
                count_eng_span[indexes] += weighted_translation / sum
                total_span[span_sorted] += np.sum(weighted_translation / sum, axis=1)
            translation_table = (count_eng_span.T / total_span).T    
    return translation_table

def generate_word_to_word_prob(translated_output, translation_table, span_dict, english_dict):
    
    span_eng_dtct = collections.defaultdict(lambda: str)
    t = codecs.open('samp.txt', 'w+', encoding='utf-8') 
    with codecs.open(translated_output, 'w+', encoding='utf-8') as trans:
        for span in span_dict:
            max = 0.0
            for eng in english_dict:
                
                prob = translation_table[span_dict[span], english_dict[eng]]
                if prob > 0:
                    if prob < CUT_OFF: 
                        prob = CUT_OFF
                    #print('pro',prob)
                    if float(prob) > float(max):
                        max = float(prob)
                        #print(max)                      
                        e = eng
                    t.write('%s %s %.15f\n' % (span, eng, prob)) 
            #print(max)
            span_eng_dtct[span] = e
            trans.write('%s %s %.15f\n' % (span, e, max)) 
    """
    for k, v in span_eng_dtct.items():
        print(k, v)
    """
    return span_eng_dtct

def generate_dev_span_to_eng(french_dev_file, span_eng_dtct):
    """
    """
    file = codecs.open('my_output.txt', 'w',encoding='utf-8')
    span_dev = codecs.open(french_dev_file, 'r+', encoding='utf-8') 
    for span_sen in span_dev.readlines():
        text = ''
        span_sen_split = span_sen.split()
        for word in span_sen_split:
            try:
                eng = span_eng_dtct.get(word)
                text += eng
                text+= ' '
            except:
                #print('ddd')               
                pass
            
        text+= '\n'
        #print(text)
        file.write(text)
    file.close()
    #span_dev.close()
def create_pos_tags():
    translated_text = open('my_output.txt', 'r')
    tag_list = []
    for line in translated_text:
        line = nltk.word_tokenize(line)
        pos_tags = nltk.pos_tag(line)
        #print(pos_tags)
        tag_list.append(pos_tags)             
    return tag_list    
    
def rearrange_based_on_pos(tag_list):    
    reordered_file = open('my_output1.txt', 'w')
    for line in tag_list: 
        #print(line)
        transformed = line
        
        transformed = reorder_noun1_of_noun2(transformed)
        transformed = remove_be_before_verbs(transformed)
        transformed = swap_nouns_adjectives(transformed)
        transformed = reorder_in_and_adverbs(transformed)
        transformed = remove_a_before_proper_nouns(transformed)
        transformed = remove_article_before_proper_noun(transformed)
        #transformed = grammarRules.fix_a_an(transformed)
        transformed = remove_consecutive_same_words(transformed)   
        transformed = switch_adverbs_and_verbs(transformed)
        #transformed = grammarRules.switch_reflexive_verbs(transformed)

        for t in transformed: 
            reordered_file.write(t[0] + ' ')
        reordered_file.write('\n')  

def reorder_noun1_of_noun2(line): 
    reordered = []
    try:
        reordered.insert(0, line[len(line)-1])
    except:
        pass
    i = len(line)-2
    prev_of = (-1, -1)
    while i >= 0: 
        if i > 0: 
            prev = line[i-1]
            curr = line[i]
            next = line[i+1]
            if curr[0] == 'of' and is_noun_not_proper(prev) and is_noun_not_proper(next): 
                if prev_of[0] == -1: # no ofs in a row
                    reordered = reordered[1:]
                    reordered.insert(0, prev)
                    reordered.insert(0, next)
                    prev_of = (0, 1)
                else: 
                    reordered.insert(prev_of[1]+1, prev)
                    prev_of = (0, prev_of[1]+1)
                i -= 1

            else: 
                reordered.insert(0, curr)
                prev_of = (-1, -1)
        else: 
            reordered.insert(0, line[i])
        i -= 1
    return reordered

def remove_be_before_verbs(line): 
    reordered = []
    index = 0
    while index < len(line): 
        curr = line[index]
        #print 'curr = ', curr
        if curr[0] == 'be' and index != len(line)-1: 
            next = line[index+1]
            if is_verb(next) is False: 
                reordered.append(curr)
        else: 
            reordered.append(curr)
        index += 1
    return reordered

def is_noun_not_proper(tup): 
    if tup[1] == 'NN' or tup[1] == 'NNS': 
        return True
    return False

def is_noun(tup): 
    if tup[1] == 'NN' or tup[1] == 'NNS' or tup[1] == 'NNP' or tup[1] == 'NNPS': 
        return True
    return False

def swap_nouns_adjectives(line): 
    reordered = line
    for i in range(1, len(reordered)): 
        curr = reordered[i]
        prev = reordered[i-1]
        if is_adjective(curr) and is_noun(prev): 
            reordered[i-1] = curr
            reordered[i] = prev
    return reordered


def is_verb(tup): 
    if tup[1] == 'VB' or tup[1] == 'VBD' or tup[1] == 'VBG' or tup[1] == 'VBN' or tup[1] == 'VBP' or tup[1] == 'VBZ': 
        return True
    return False

def is_adjective(tup): 
    return tup[1] == 'JJ'

def is_adverb(tup): 
    return tup[1] == 'RB'

def is_proper_noun(tup): 
    if tup[1] == 'NNP' or tup[1] == 'NNPS': 
        return True
    return False

def reorder_in_and_adverbs(line): 
    reordered = line
    in_index = -1
    adverbs_present = False
    in_list = []
    adverb_list = []
    i = 0
    while i < len(line):
        curr = line[i]
        if curr[0] == 'in': 
            in_index = i
            in_list.append(curr)

        else: 
            if is_adverb(curr): 
                adverb_list.append(curr)
                adverbs_present = True
            else: 
                if in_index != -1 and adverbs_present is False: 
                    in_list.append(curr)
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

def remove_a_before_proper_nouns(line): 
    reordered = []
    index = 1
    try:
        reordered.append(line[0])
    except:
        pass
    while index < len(line)-1: 
        curr = line[index]
        prev = line[index-1]
        next = line[index+1]
        if curr[0] == 'at': 
            if is_proper_noun(next) is False:# or is_verb(prev) is False: 
                # commented out is_verb(prev) because the POS tag for prev is often wrong
                reordered.append(curr)
        else: 
            reordered.append(curr)
        index += 1
    try:
        reordered.append(line[len(line)-1])
    except:
        pass
    return reordered

def remove_article_before_proper_noun(line): 
    reordered = []
    index = 0
    while index < len(line): 
        curr = line[index]
        #print 'curr = ', curr
        if curr[1] == 'DT' and index != len(line)-1: 
            next = line[index+1]
            if is_proper_noun(next) is False: 
                reordered.append(curr)
        else: 
            reordered.append(curr)
        index += 1
    return reordered

def swap_verbs_personal_pronouns(line): 
    reordered = line
    for i in range(1, len(reordered)): 
        curr = reordered[i]
        prev = reordered[i-1]
        if is_verb(curr) and prev[1] == 'PRP': 
            reordered[i-1] = curr
            reordered[i] = prev
    return reordered

def fix_a_an(line): 
    reordered = line
    for i in range(0, len(reordered)): 
        curr = reordered[i]
        if curr[0] == 'a' and i < len(reordered)-1:
            next = reordered[i+1]
            if is_vowel(next[0][0]): 
                reordered[i] = ('an', 'DT')
        if curr[0] == 'an' and i < len(reordered)-1: 
            next = reordered[i+1]
            if is_vowel(next[0][0]) is False:
                reordered[i] = ('a', 'DT')
    return reordered

def is_vowel(ch):
    if ch == 'a' or ch == 'e' or ch == 'i' or ch == 'o' or ch == 'u': 
        return True
    return False

def remove_consecutive_same_words(line): 
    prev_word = ''
    reordered = []
    try:
        reordered.append(line[0])
    except:
        pass
    for i in range(1, len(line)): 
        curr = line[i]
        prev = line[i-1]
        if curr[0] != prev[0]: 
            reordered.append(curr)
    return reordered

def switch_adverbs_and_verbs(line):
    reordered = []
    i = 0
    while i < len(line)-1:
        currTuple = line[i]
        currWord = currTuple[0]
        if is_verb(currTuple):
            nextTuple = line[i+1]
            nextWord = nextTuple[0]
            if is_adverb(nextTuple):
                #print(currWord + ' ' + nextWord)
                reordered.append(nextTuple)
                reordered.append(currTuple)
                i += 1
            else: 
                reordered.append(currTuple)
        else:
            reordered.append(line[i])
        i += 1
    try:
        reordered.append(line[len(line)-1])
    except:
        pass
    return reordered


def switch_reflexive_verbs(line):
    reordered = []
    i = 0
    while i < len(line):
        currTuple = line[i]
        currWord = currTuple[0]
        if currTuple[1] == 'PRP':
            nextTuple = line[i+1]
            nextWord = nextTuple[0]
            if is_verb(nextTuple):
                print(currWord + ' ' + nextWord)
                reordered.append(nextTuple)
                reordered.append(currTuple)
                i += 1
        else:
            reordered.append(line[i])
        i += 1
    return reordered
   
if __name__ == "__main__":
    english_dict,eng_count =  generate_english_vocab(english_file)
    #print(pairs)
    span_dict, count, span_count = generate_french_vocab(french_file)
    translation_table = init_translation_table(span_count, eng_count)
    translation_table = populate_translation_table(english_dict,eng_count,span_dict, count, span_count, translation_table )
    #print(translation_table)
    span_eng_dtct = generate_word_to_word_prob(translated_output, translation_table, span_dict, english_dict)
    generate_dev_span_to_eng(french_dev_file, span_eng_dtct)
    #tag_list =create_pos_tags()
    #rearrange_based_on_pos(tag_list)