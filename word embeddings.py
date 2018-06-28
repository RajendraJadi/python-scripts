# -*- coding: utf-8 -*-
"""
Rajendra Jadi
801023390
"""

from numpy import dot, float32 as REAL, sqrt, newaxis, ndarray, prod
from gensim import utils, matutils  # utility fnc for pickling, common scipy operations etc
from six import string_types
from six.moves import xrange
import gensim

class KeyedVectors(utils.SaveLoad):

    def __init__(self):
        self.syn0 = []
        self.syn0norm = None
        self.vocab = {}
        self.index2word = []
        self.vector_size = None
        
	
    def word_vec(self, word, use_norm=False):
        if word in self.vocab:
            if use_norm:
                result = self.syn0norm[self.vocab[word].index]
            else:
                result = self.syn0[self.vocab[word].index]

            result.setflags(write=False)
            return result

    def init_sims(self, replace=False):
        if getattr(self, 'syn0norm', None) is None or replace:
            #logger.info("precomputing L2-norms of word weight vectors")
            if replace:
                for i in xrange(self.syn0.shape[0]):
                    self.syn0[i, :] /= sqrt((self.syn0[i, :] ** 2).sum(-1))
                self.syn0norm = self.syn0
            else:
                self.syn0norm = (self.syn0 / sqrt((self.syn0 ** 2).sum(-1))[..., newaxis]).astype(REAL)			

#Find Cosine similarity between two vectors using Mekolov model
    def most_similar_cosmul(self, positive, negative, topn=10):
        if positive is None:
            positive = [0, 0 ,0]
        if negative is None:
            negative = [0,0,0]
        
        #self.init_sims()

        if isinstance(positive, string_types) and not negative:
            # allow calls like most_similar_cosmul('dog'), as a shorthand for most_similar_cosmul(['dog'])
            positive = [positive]

        all_words = {self.vocab[word].index for word in positive + negative  if not isinstance(word, ndarray) and word in self.vocab   }

        positive = [self.word_vec(word, use_norm=True) if isinstance(word, string_types) else word  for word in positive  ]
        negative = [self.word_vec(word, use_norm=True) if isinstance(word, string_types) else word for word in negative    ]

        if not positive:
            raise ValueError("cannot compute similarity with no input")

        pos_dists = [((1 + dot(self.syn0norm, term)) / 2) for term in positive]
        neg_dists = [((1 + dot(self.syn0norm, term)) / 2) for term in negative]
        dists = prod(pos_dists, axis=0) / (prod(neg_dists, axis=0) + 0.000001)
        if not topn:
            return dists
        best = matutils.argsort(dists, topn=topn + len(all_words), reverse=True)
        # ignore (don't return) words from the input
        result = [(self.index2word[sim], float(dists[sim])) for sim in best if sim not in all_words]
        return result[:topn]

def main():
# Load pretrained model (since intermediate data is not included, the model cannot be refined with additional data)
    model = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True,limit=3010000)
    #print(model.wv['computer'])
    #train_text = open('train.txt', 'r')
    #mv = KeyedVectors()
    count =0
    total =0
    accuracy=0
    
    for line in open('train2.txt', 'r'):
        line =' '.join(line.split())
        line = line.strip()
        if not line.startswith(":"):
            line=line.split(" ")
            total = total +1
            print(" ")
            print(line)
            predict = (model.wv.most_similar_cosmul(positive=[line[1], line[2]], negative=[line[0]])) 
        
            for i in predict :
                if line[3] in i:
                    print(i)
                    count = count + 1
                    print("Correct: ",count)
            
    print("Analogies Correctly predictedcount: ",count)
    print("Total numbelr of analogies in the test set: ",total)
    accuracy = (count/total)*100
    print("Accuracy of the Word2Vec model using GoogleNews-Vectors: ", round(accuracy,2),"%")   
    return

def gloVe():
# Load pretrained model (since intermediate data is not included, the model cannot be refined with additional data)
    model = gensim.models.KeyedVectors.load_word2vec_format('glove.42B.300d.txt', binary=False,limit=3010000)
    count =0
    total =0
    accuracy=0
    
    for line in open('train2.txt', 'r'):
        line =' '.join(line.split())
        line = line.strip()
        if not line.startswith(":"):
            line=line.split(" ")
            total = total +1
            print(" ")
            print(line)
            predict = (model.wv.most_similar_cosmul(positive=[line[1], line[2]], negative=[line[0]])) 
        
            for i in predict :
                if line[3] in i:
                    print(i)
                    count = count + 1
                    print("Correct: ",count)
            
    print("Analogies Correctly predictedcount: ",count)
    print("Total numbelr of analogies in the test set: ",total)
    accuracy = (count/total)*100
    print("Accuracy of the Word2Vec model using GloVe: ", round(accuracy,2),"%")   
    return

if __name__ == "__main__":
    main()
    gloVe()

    