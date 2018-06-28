"""
Assignmet4: Classification
Rajendra Jadi
801023390
"""

import re
import string
import collections
from collections import Counter
import nltk
import math
    
def train():
    file = open('train','r')
    speakers=[]
    comments={}
    for line in file:
        temp = nltk.word_tokenize(line)[0]
        if temp not in speakers:
            speakers.append(temp)
        line=line.split(' ')
        line=[''.join(c for c in s if c not in [',','.','?',':',';','!']) for s in line]
        line=[s for s in line if s!='' and s!='\n']
            
        if(line[0] not in comments):
            comments.setdefault(line[0],[])
        comments[line[0]].append(line[1:])

    training_prob={}
    word_prob={}

    dict_word={}
    dict_doc={}
    dict_prev={}
    words={}
    for speaker in speakers:
        a1=[]
        a2=[]
        dict_word.setdefault(speaker,0)
        words.setdefault(speaker,[])
        dict_doc.setdefault(speaker,0)
        for array in comments.get(speaker):
            a2.append(array)
            for word in array:
                a1.append(word)
                words[speaker].append(word)
        dict_word[speaker]=len(a1)
        dict_doc[speaker]=len(a2)
  
    for speaker in speakers:
        dict_prev.setdefault(speaker,0)
        dict_prev[speaker]=dict_doc[speaker]/(sum(dict_doc.values()))
  
    all_words=[]
    for array in words.values():
        for word in array:
            all_words.append(word)
            
    V = []
    for word in line:
        if word not in V:
            V.append(word);
      
    length=len(list(set(all_words)))

    prob_count=0
    list_ = []
    for speaker in speakers:
        training_prob.setdefault(speaker,{})
        word_prob={}
        for word in list(set(words[speaker])):
            prob_count=(words[speaker].count(word)+0.14)/(dict_word[speaker]+(length*0.14))
            word_prob[word]=prob_count
        word_prob[' ']=1/(dict_word[speaker]+(length*0.14))
        training_prob[speaker]=word_prob   
        list_ = sorted(word_prob, key=word_prob.get, reverse=True)[:20]   
        print(speaker)
        for li in list_:
            print('"',li,'",',end="")
        print('\n')
        for li in list_:
            print(word_prob[li],',',end="")
        print('\n')         
    #print(speaker,training_prob[speaker])
    
    #print(_lst)
    
    return training_prob,dict_prev,speakers;
        
def test(training_prob,dict_prev,speakers):
    test_prob={}
    for speaker in speakers:
        test_prob.setdefault(speaker,[])
        file = open('test','r')
        for line in file: 
            line=line.split(' ')
            line=[''.join(c for c in s if c not in [',','.','?',':',';']) for s in line]
            line=[s for s in line if s!='' and s!='\n']
            #prob_test_value=0
            temp=[]
            for test_word in line[1:]:   
                if(test_word in training_prob.get(speaker)):
                    temp.append(math.log(training_prob.get(speaker)[test_word]))
                else:
                     temp.append(math.log(training_prob.get(speaker)[' ']))
                        
            a=(sum(temp)+math.log(dict_prev[speaker]))
            test_prob[speaker].append(a)
                        
    speakers=test_prob.keys()
    sentence_speaker = ''
    classified_speaker = []
    for i in range(400):
        max = test_prob.get('sanders')[i]
        for k, v in test_prob.items():
            if v[i]>=max:
                max = v[i]
                sentence_speaker = k
        classified_speaker.append(sentence_speaker)
  
    total_count_test = 0
    correct = 0
    #loop_count = 0
    file = open('test','r')
    for line in file:
        line=line.split(' ')
        line=[''.join(c for c in s if c not in [',','.','?',':',';']) for s in line]
        line=[s for s in line if s!='' and s!='\n']
        if(line[0] == classified_speaker[total_count_test]):
            correct += 1
        total_count_test += 1


      
    print("Classification accuracy of Naive-Bayes is:  ", ((correct/total_count_test)*100),"%")
    return;




def binary_train():
    file = open('train','r')
    speakers=[]
    comments={}
    for line in file:
        temp = nltk.word_tokenize(line)[0]
        if temp not in speakers:
            speakers.append(temp)
        line=line.split(' ')
        line=[''.join(c for c in s if c not in [',','.','?',':',';','!']) for s in line]
        line=[s for s in line if s!='' and s!='\n']
            
        if(line[0] not in comments):
            comments.setdefault(line[0],[])
        comments[line[0]].append(line[1:])

    training_prob={}
    word_prob={}

    dict_word={}
    dict_doc={}
    dict_prev={}
    words={}
    for speaker in speakers:
        a1=[]
        a2=[]
        dict_word.setdefault(speaker,0)
        words.setdefault(speaker,[])
        dict_doc.setdefault(speaker,0)
        for array in comments.get(speaker):
            a2.append(array)
            for word in list(set(array)):
                a1.append(word)
                words[speaker].append(word)
        dict_word[speaker]=len(a1)
        dict_doc[speaker]=len(a2)
  
    for speaker in speakers:
        dict_prev.setdefault(speaker,0)
        dict_prev[speaker]=dict_doc[speaker]/(sum(dict_doc.values()))
  
    all_words=[]
    for array in words.values():
        for word in array:
            all_words.append(word)
            
    V = []
    for word in line:
        if word not in V:
            V.append(word);
      
    length=len(list(set(all_words)))

    prob_count=0

    for speaker in speakers:
        training_prob.setdefault(speaker,{})
        word_prob={}
        for word in list(set(words[speaker])):
            prob_count=(words[speaker].count(word)+0.17)/(dict_word[speaker]+(length*0.17))
            word_prob[word]=prob_count
        word_prob[' ']=1/(dict_word[speaker]+(length*0.17))
        training_prob[speaker]=word_prob               
    
    return training_prob,dict_prev,speakers;
        
def binary_test(training_prob,dict_prev,speakers):
    test_prob={}
    for speaker in speakers:
        test_prob.setdefault(speaker,[])
        file = open('test','r')
        for line in file: 
            line=line.split(' ')
            line=[''.join(c for c in s if c not in [',','.','?',':',';']) for s in line]
            line=[s for s in line if s!='' and s!='\n']
            #prob_test_value=0
            temp=[]
            for test_word in line[1:]:   
                if(test_word in training_prob.get(speaker)):
                    temp.append(math.log(training_prob.get(speaker)[test_word]))
                else:
                     temp.append(math.log(training_prob.get(speaker)[' ']))
                        
            a=(sum(temp)+math.log(dict_prev[speaker]))
            test_prob[speaker].append(a)
                        
    speakers=test_prob.keys()
    sentence_speaker = ''
    classified_speaker = []
    for i in range(400):
        max = test_prob.get('sanders')[i]
        for k, v in test_prob.items():
            if v[i]>=max:
                max = v[i]
                sentence_speaker = k
        classified_speaker.append(sentence_speaker)
  
    total_count_test = 0
    correct = 0
    #loop_count = 0
    file = open('test','r')
    for line in file:
        line=line.split(' ')
        line=[''.join(c for c in s if c not in [',','.','?',':',';']) for s in line]
        line=[s for s in line if s!='' and s!='\n']
        if(line[0] == classified_speaker[total_count_test]):
            correct += 1
        total_count_test += 1


      
    print("Classification accuracy of Binary Naive Bayes is:  ", ((correct/total_count_test)*100),"%")
    return;


def bigram_train():
    file = open('train','r')
    bigram_words = {}
    bigram_word_count = {}
    speakers=[]
    comments={}
    comments_bigrams = {}
    for line in file:
        temp = nltk.word_tokenize(line)[0]
        if temp not in speakers:
            speakers.append(temp)
        line=line.split(' ')
        line=[''.join(c for c in s if c not in [',','.','?',':',';','!']) for s in line]
        line=[s for s in line if s!='' and s!='\n']
            
        if(line[0] not in comments):
            comments.setdefault(line[0],[])
            comments_bigrams.setdefault(line[0], [])
        comments[line[0]].append(line[1:])
        comments_bigrams[line[0]].append(nltk.ngrams(line[1:], 2))

    training_prob={}
    word_prob={}

    dict_word={}
    dict_doc={}
    dict_prev={}
    words={}
    for speaker in speakers:
        a1=[]
        a2=[]
        a3 =[]
        dict_word.setdefault(speaker,0)
        words.setdefault(speaker,[])
        bigram_words.setdefault(speaker, [])
        dict_doc.setdefault(speaker,0)
        for array,array2 in zip(comments.get(speaker),comments_bigrams.get(speaker)):
            a2.append(array)
            for word in array:
                a1.append(word)
                words[speaker].append(word)
            for bigram in array:
                a3.append(bigram)
                bigram_words[speaker].append(bigram)
                
                
        dict_word[speaker]=len(a1)
        dict_doc[speaker]=len(a2)
        bigram_word_count[speaker] = len(a3)
  
    for speaker in speakers:
        dict_prev.setdefault(speaker,0)
        dict_prev[speaker]=dict_doc[speaker]/(sum(dict_doc.values()))
  
    all_words=[]
    for array in words.values():
        for word in array:
            all_words.append(word)
            
    V = []
    for word in line:
        if word not in V:
            V.append(word);
      
    length=len(list(set(all_words)))

    prob_count=0
    alpha = 0.14
    for speaker in speakers:
        training_prob.setdefault(speaker,{})
        word_prob={}
        for word in list(set(bigram_words[speaker])):
           prob_count=(bigram_words[speaker].count(word) + 0.18)/(words[speaker].count(word[0]) + (length * 0.18))
           word_prob[word]=prob_count
        word_prob[' ']=alpha/(bigram_word_count[speaker] + (length * alpha))
        training_prob[speaker]=word_prob               
    
    return training_prob,dict_prev,speakers;
        
def bigram_test(training_prob,dict_prev,speakers):
    test_prob={}
    
    for speaker in speakers:
        test_prob.setdefault(speaker,[])
        file = open('test','r')
        for line in file: 
            line=line.split(' ')
            line=[''.join(c for c in s if c not in [',','.','?',':',';']) for s in line]
            line=[s for s in line if s!='' and s!='\n']
            
            bigram_line = nltk.ngrams(line[1:], 2)
            #prob_test_value=0
            temp=[]
            for test_bigram in bigram_line:   
                if(test_bigram in training_prob.get(speaker)):
                    temp.append(math.log(training_prob.get(speaker)[test_bigram]))
                else:
                     temp.append(math.log(training_prob.get(speaker)[' ']))
                        
            a=(sum(temp)+math.log(dict_prev[speaker]))
            test_prob[speaker].append(a)
                        
    speakers=test_prob.keys()
    
    sentence_speaker = ''
    classified_speaker = []
    c = 200
    for i in range(400):
        max = test_prob.get('sanders')[i]
        for k, v in test_prob.items():
            if v[i]>=max:
                max = v[i]
                sentence_speaker = k
        classified_speaker.append(sentence_speaker)
        
    V = []
    for word in line:
        if word not in V:
            V.append(word);
            
    total_count_test = 0
    
    #loop_count = 0
    file = open('test','r')
    for line in file:
        line=line.split(' ')
        line=[''.join(c for c in s if c not in [',','.','?',':',';']) for s in line]
        line=[s for s in line if s!='' and s!='\n']
        if(line[0] == classified_speaker[total_count_test]):
            c += 1
        total_count_test += 1


      
    print("Classification accuracy of Naive-Bayes using Bi-gram is:  ", ((c/total_count_test)*100),"%")
    return;


training_prob,dict_prev,speakers = train()
test(training_prob,dict_prev,speakers)

training_prob,dict_prev,speakers = binary_train()
binary_test(training_prob,dict_prev,speakers)

training_prob,dict_prev,speakers = bigram_train()
bigram_test(training_prob,dict_prev,speakers)



