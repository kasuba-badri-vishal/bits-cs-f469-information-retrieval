import numpy as np
from pandas import DataFrame

class VectorSpaceModel(DataFrame):
    
    def __init__(self, corpus, collection_freq):
        #default constructor
        DataFrame.__init__(self,index=list(collection_freq.keys()), columns=np.arange(0,len(corpus)))
    
        self.max_freq = 100
        for word in self.index:
            for i in range(len(corpus)):
                self.loc[word][i] = self.tf_idf(word, corpus[i], corpus)

    def term_freq(self, word, document):
        """
            Returns the frequency of the word as logarithm(No of occurences in the document)
            by using the word_freq dictionary  
        """
        if word in document.word_freq:
            return (1+np.log10(document.word_freq[word]))
        else:
            return 0
    
    def doc_freq(self, word, corpus):
        """
            Returns the count of all the documents(which are part of corpus) 
            in which the word occurs
        """
        count = 0
        for doc in corpus:
            if word in doc.word_freq:
                count += 1
        return count

    def idf(self, word, corpus):
        """
        Returns the Inverse Document Frequency (idf) of a word 
          idf = Logarithm ((Total Number of Documents) /  
            (Number of documents containing the word)) 
        """
        idf = self.doc_freq(word, corpus)
        if idf == 0: 
            return 0
        return np.log10(len(corpus)/(idf))           
    
    def tf_idf(self, word, document, corpus):
        """
        tf_idf(word, document) = term frequency(word, document)* inverse document freq(word, document)
        """
        return self.term_freq(word, document)*self.idf(word, corpus)
    
    def cosine_sim(self, a, b):
        """
        Returns the cosine or the dot product of two vectors(query and document or
        document and document)
        """
        return np.dot(a,b)

    def search(self, qdoc, corpus):
        """
            Input: Query(also a document)
            Returns: Sorted rank of documents according to the tf-idf value (in descending order) 
        """
        q_vec = np.ndarray((self.shape[0], ))
        for i,word in enumerate(self.index):
            q_vec[i] = self.tf_idf(word, qdoc, corpus)

        res = []

        for i in self.columns:
            res.append((self.cosine_sim(q_vec, self[i]),i))
        return sorted(res, key=lambda x: x[0], reverse=True)
            