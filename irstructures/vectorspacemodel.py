import numpy as np
from pandas import DataFrame

class VectorSpaceModel(DataFrame):
    
    def __init__(self, corpus, collection_freq):
        DataFrame.__init__(self,index=list(collection_freq.keys()), columns=np.arange(0,len(corpus)))
        # self.max_freq = int(np.max(list(collection_freq.values())))
        self.max_freq = 100
        for word in self.index:
            for i in range(len(corpus)):
                # if word in corpus[i].word_freq:
                self.loc[word][i] = self.tf_idf(word, corpus[i], corpus)
                # else 
                #     self.loc[word][i] = 0


    def term_freq(self, word, document):
        if word in document.word_freq:
            return (1+np.log10(document.word_freq[word]))
        else:
            return 0
    
    def doc_freq(self, word, corpus):
        c = 0
        for doc in corpus:
            if word in doc.word_freq:
                c += 1
        return c

    def idf(self, word, corpus):
        idf = self.doc_freq(word, corpus)
        if idf == 0: 
            return 0
        return np.log10(len(corpus)/(idf))           
    
    def tf_idf(self, word, document, corpus):
        return self.term_freq(word, document)*self.idf(word, corpus)
    
    def cosine_sim(self, a, b):
        return np.dot(a,b)

    def search(self, qdoc, corpus):
        q_vec = np.ndarray((self.shape[0], ))
        for i,word in enumerate(self.index):
            q_vec[i] = self.tf_idf(word, qdoc, corpus)

        res = []

        for i in self.columns:
            res.append((self.cosine_sim(q_vec, self[i]),i))
        return sorted(res, key=lambda x: x[0], reverse=True)
            