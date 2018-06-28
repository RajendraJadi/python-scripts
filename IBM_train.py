from __future__ import division
from collections import Counter
from math import log
import numpy as np
import codecs
import sys




frenchfile = "fr-en\\train\\europarl-v7.fr-en.fr"
englishfile = "fr-en\\train\\europarl-v7.fr-en.en"
translationoutput = "IBM_translation.txt"


pairs = [] 
eng = {}
engcnt = 0
with codecs.open(englishfile, encoding='utf-8') as E:
    for e in E:
        s = e.lower().split()
        pairs.append([s])

        
        for w in s:
            if w not in eng:
                eng[w] = engcnt
                engcnt += 1

fr = {} 
cnt = 0 
frcnt = 0 
with codecs.open(frenchfile, encoding='utf-8') as F:
    for f in F:
        s = f.lower().split()
        s.append("null")
        pairs[cnt].append(s)
        cnt += 1

       
        for w in s:
            if w not in fr:
                fr[w] = frcnt
                frcnt += 1


translate_table = np.ones([frcnt, engcnt]) / engcnt

iterations = 0
old_likelihood = -2 # dummy values
new_likelihood = -1

epsilon = 10**(-5)
while iterations < 2 or abs(new_likelihood - old_likelihood) > epsilon:    

        iterations += 1        
        if iterations > 1: old_likelihood = new_likelihood

        if iterations > 30: break

        ## E-STEP
        new_likelihood = 0
        count_e_f = np.zeros([frcnt, engcnt])
        total_f = np.zeros(frcnt)        

        for pair in pairs:

            
            indeng = Counter([eng[p] for p in pair[0]])            
            indfr  = Counter([fr[p] for p in pair[1]])            

            
            sortedeng = sorted(indeng)
            sortedfr = sorted(indfr)
            indexes = np.ix_(sortedfr, sortedeng)
            weighted_translation = translate_table[indexes]

            for pos, y in enumerate(sortedeng): 
                if indeng[y] > 1: weighted_translation[:, pos] *= indeng[y]           

            for pos, y in enumerate(sortedfr): 
                if indfr[y] > 1:  weighted_translation[pos, :] *= indfr[y]           

            
            z = np.sum(weighted_translation, axis=0)

            
            new_likelihood += np.sum(np.log(z))
            
            # Collect counts.
            temp = weighted_translation / z
            count_e_f[indexes] += temp
            total_f[sortedfr] += np.sum(temp, axis=1)

        ## M-STEP
        translate_table = (count_e_f.T / total_f).T
        #print iterations, new_likelihood, new_likelihood - old_likelihood



print("EM converged.")
print("Writing translation probabilities to the output file...")
minpr = 10 ** (-15)
with codecs.open(translationoutput, 'w+', encoding='utf-8') as T:
    for f in fr:
        for e in eng:
            pr = translate_table[fr[f], eng[e]]
            if pr > 0:
                if pr < minpr: pr = minpr
                T.write('%s %s %.15f\n' % (f, e, pr))
print("Training done")

