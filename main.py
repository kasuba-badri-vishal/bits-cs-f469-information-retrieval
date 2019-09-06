from irstructures.document import Document, read_corpus, read_query
from irstructures.logger import Logger
from irstructures.invertedindex import InvertedIndex
from irstructures.vectorspacemodel import VectorSpaceModel
import pandas as pd
import numpy as np

print("\n***Program started***\n")

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

while True:
    query = input("Enter query: ")
    if query == "EXIT":
        break
    else:
        q = read_query(query)
        print(df.search(q,corpus))
        

print("\n***End of program***\n")