from nltk.tokenize import wordpunct_tokenize, word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import os

# TODO: remove dependancy on nltk and use stemmer:porter file and tokenizer:regex for wordpunct_tokenize

class Document:

    document_count = 0
    stemmer = PorterStemmer()
    stop_words = set(stopwords.words('english'))
    stop_words.update( ['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', 
                        '[', ']', '{', '}', '`', '``', "'s", "''", "m", "re", "s"
                        'es' ])

    def __init__(self, filepath=None, doc_id=None, raw_data="", use_regex=False, stemming=True):
        """
        Attributes of Document object
            filepath: filepath to document
            raw_data: data present in document without any modifications
            data: normalized data
            words: list of all words present in document
            word_freq: dictionary of words and their frequency
        """
        self.filepath = filepath
        self.raw_data = raw_data
        Document.document_count += 1
        if doc_id is None:
            self.doc_id = Document.document_count
        else:
            self.doc_id = doc_id
        
        # Read data from file if object is not given any data
        if filepath is not None:
            with open(filepath, 'r') as file:
                self.raw_data = file.read()
        
        # reduce caps and TODO:remove accents
        self.data = self.raw_data.lower()
        
        # tokenize words
        if use_regex is True:
            self.words = wordpunct_tokenize(self.data)
        else:
            self.words = word_tokenize(self.data)
        
        # remove stop words
        self.words = [word for word in self.words if word not in Document.stop_words]

        # run porter stemmer
        if stemming is True:
            self.words = [Document.stemmer.stem(word) for word in self.words]

        # create a dictionary to store words and their frequencies
        self.word_freq = dict()
        for word in self.words:
            self.word_freq[word] = (self.word_freq[word]+1) if word in self.word_freq else 1



# use this function to read complete corpus
def read_corpus(folderpath, log_level=5):
    # TODO: check if folder path exists
    from .logger import Logger
    logger = Logger(log_level)
    files = []
    document_list = []
    logger.log("Reading corpus", 1)
    # r=root, d=directories, f=files
    for r, d, f in os.walk(folderpath):
        for filename in f:
            if '.txt' in filename:
                files.append(os.path.join(r,filename))
    
    for file in files:
        document_list.append(Document(file))
        logger.log("file read: "+file, 6)
    
    return document_list

def read_query(query):
    return Document(raw_data=query)


# if __name__ == "__main__":
#     print("***Testing Document class***")
#     data = input("give data input: ")
#     document = Document(raw_data=data)