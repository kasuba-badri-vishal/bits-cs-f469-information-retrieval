from irstructures.document import Document, read_corpus, read_query
from irstructures.logger import Logger
from irstructures.vectorspacemodel import VectorSpaceModel
import pandas as pd
import numpy as np
import pickle
import os
import time

def start_search(df, corpus):
    while True:
        query = input("Enter query: ")
        if query == "EXIT":
            break
        else:
            q = read_query(query)
            print()
            doc_num = 0
            start_time = time.time()
            for d in df.search(q, corpus):
                if d[0]!=0:
                    doc_num+=1
                    print(str(doc_num)+")",corpus[d[1]].filepath)
                    if doc_num==10:
                        break
            end_time = time.time()
            print("\nNumber of documents returned: ",doc_num,"\n")
            print("Time taken: {0}s\n".format(end_time-start_time))


if __name__=="__main__":

    print("\n***Program started***\n")

    if("vectorspace_pickle" in os.listdir(".")) and ("corpus_pickle" in os.listdir(".")):
        # if pickle files are found

        # loading vectorspacemodel
        vectorspace_file = open("vectorspace_pickle", "rb")
        df = pickle.load(vectorspace_file)
        vectorspace_file.close()
        # loading corpus
        corpus_file = open("corpus_pickle", "rb")
        corpus = pickle.load(corpus_file)
        corpus_file.close()
        
        start_search(df, corpus)

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
        vectorspace_file = open("vectorspace_pickle", "wb")
        pickle.dump(df, vectorspace_file)
        vectorspace_file.close()

        corpus_file = open("corpus_pickle", "wb")
        pickle.dump(corpus, corpus_file)
        corpus_file.close()

        start_search(df, corpus)
    print("\n***End of program***\n")
    
