from irstructures.document import Document, read_corpus, read_query
from irstructures.logger import Logger
from irstructures.invertedindex import InvertedIndex
from irstructures.vectorspacemodel import VectorSpaceModel
import pandas as pd
import numpy as np
import pickle
import os

if __name__=="__main__":

    print("\n***Program started***\n")

    if("vectorspace" in os.listdir(".")) and ("corpus_pickle" in os.listdir(".")):
        # if pickle files are found

        # loading vectorspacemodel
        vectorspace_file = open("vectorspace", "rb")
        df = pickle.load(vectorspace_file)
        vectorspace_file.close()
        # loading corpus
        corpus_file = open("corpus_pickle", "rb")
        corpus = pickle.load(corpus_file)
        corpus_file.close()
        while True:
            query = input("Enter query: ")
            if query == "EXIT":
                break
            else:
                q = read_query(query)
                print()
                for d in df.search(q,corpus):
                    if d[0]!=0:
                        print(corpus[d[1]].filepath)
                print()
    else:
        # if no pickle files are found

        # using logger class to print statements based on level.
        logger = Logger(6)
        # folder name is corpus in this case
        corpus = read_corpus('corpus', logger.level)
        logger.log("Total documents read: "+str(Document.document_count))

        logger.log("Calculating collection frequency", 1)
        collection_freq = dict()
        for document in corpus:
            for word in document.word_freq:
                if word in collection_freq:
                    collection_freq[word] += document.word_freq[word]
                else:
                    collection_freq[word] = document.word_freq[word]


        logger.log("Writing word collection to disk", 1)

        with open("word_collection.txt", 'w') as file:
            for word in collection_freq:
                file.write(word + "\n"  )

        df = VectorSpaceModel(corpus, collection_freq)

        # writing vectorspacemodel and corpus to pickle files
        vectorspace_file = open("vectorspace", "wb")
        pickle.dump(df, vectorspace_file)
        vectorspace_file.close()

        corpus_file = open("corpus_pickle", "wb")
        pickle.dump(corpus, corpus_file)
        corpus_file.close()

        while True:
            query = input("Enter query: ")
            if query == "EXIT":
                break
            else:
                q = read_query(query)
                print(df.search(q,corpus))

    print("\n***End of program***\n")
    
