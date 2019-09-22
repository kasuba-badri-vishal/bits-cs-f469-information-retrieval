from .document import Document
from .logger import Logger

class InvertedIndex(dict):
    def __init__(self, corpus, collection_freq=None):
        for document in corpus:
            for word in document.word_freq:
                if word in self:
                    self[word].append(document.doc_id)
                else:
                    self[word] = [document.doc_id]