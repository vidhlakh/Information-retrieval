

'''

Index structure:

    The Index class contains a list of IndexItems, stored in a dictionary type for easier access

    each IndexItem contains the term and a set of PostingItems

    each PostingItem contains a document ID and a list of positions that the term occurs

'''

from doc import Document
import sys
from util import isStopWord
from util import stemming
from cran import CranFile
from doc import Collection
from nltk.tokenize import RegexpTokenizer
import json

class Posting:
    def __init__(self, docID):
        self.docID = docID
        self.positions = []

    def append(self, pos):
        self.positions.append(pos)

    def sort(self):
        ''' sort positions'''
        self.positions.sort()

    def merge(self, positions):
        self.positions.extend(positions)

    def term_freq(self):
        ''' return the term frequency in the document'''
        #ToDo


class IndexItem:
    def __init__(self, term):
        self.term = term
        self.posting = {} #postings are stored in a python dict for easier index building
        self.sorted_postings= [] # may sort them by docID for easier query processing

    def add(self, docid, pos):
        ''' add a posting'''
        
        if not self.posting.__contains__(docid):
            post=Posting(docid)
            post.append(pos)
            self.posting.update({docid:post.positions})
            
        else:
            self.posting[docid].append(pos)
            
    def sort(self):
        ''' sort by document ID for more efficient merging. For each document also sort the positions'''
        # ToDo


class InvertedIndex:

    def __init__(self):
        self.items = {} # list of IndexItems
        self.nDocs = 0  # the number of indexed documents
        self.term_freq={}
        self.len_body=0
    def indexDoc(self, doc): # indexing a Document object
        ''' indexing a docuemnt, using the simple SPIMI algorithm, but no need to store blocks due to the small collection we are handling. Using save/load the whole index instead'''
        listoftokens=[]
        listofterms=[]
        psdocpos={}
        values=[]
        #tokenize the document body
        tokenizer = RegexpTokenizer(r'\w+')
        tokens = tokenizer.tokenize(doc.body)
        self.len_body=len(tokens)
        listoftokens+=tokens
        
       
            
        '''replace the token after stemming '''       
        for counter,token in enumerate(tokens):
            #self.tf=0
            stemmed_term = stemming(token)
            posi=counter
            tokens[counter]=stemmed_term  
            #remove stop words from token
            token_is_stopword=isStopWord(token)
            if(token_is_stopword):
                tokens.pop(counter)
                continue
             
            
            
            
            indexitem = IndexItem(stemmed_term)
            indexitem.add(doc.docID,posi)
            
            psdocpos= {doc.docID:[posi]}
            
            ''' if document contains the term'''
            if  self.items.__contains__(stemmed_term):
                
                #if same term in same document
                if(self.items[stemmed_term].__contains__(doc.docID)):
                    self.tf+=1/self.len_body
                    values=self.items.get(stemmed_term)
                    values[doc.docID].append(posi)
                    val=self.term_freq.get(stemmed_term)
                    val[doc.docID]=self.tf
                #if same term in different document    
                else:
                    self.tf=1/self.len_body
                    self.items[stemmed_term].update(psdocpos)
                    self.term_freq[stemmed_term].update({doc.docID:self.tf})
            #insert the new term and posting    
            else:
                self.tf=1/self.len_body
                self.items.update({stemmed_term:psdocpos}) 
                self.term_freq.update({stemmed_term:{doc.docID:self.tf}})
        listofterms+=tokens
        
        
        

    def sort(self):
        ''' sort all posting lists by docID'''
        #ToDo

    def find(self, term):
        if self.items.__contains__(term):
            return self.items[term]
        else:
            return None

    def save(self, filename):
        ''' save to disk'''
        # ToDo: using your preferred method to serialize/deserialize the index
        with open(filename, "w") as write_file:
            json.dump(self.items, write_file,indent=4,sort_keys=True)
        with open("termfreqFile", "w") as write_file:
            json.dump(self.term_freq, write_file,indent=4,sort_keys=True)
    def load(self, filename):
        ''' load from disk'''
        # ToDo
        with open(filename, "r") as read_file:
            data = json.load(read_file)
        
            
    def term_Freq_find(self, term):
        '''return the term frequency for the specific term'''
        if(self.term_freq.__contains__(term)):
            return self.term_freq[term]
        else:
            return None
    def idf(self, term):
        ''' compute the inverted document frequency for a given term'''
        #ToDo: return the IDF of the term
        

    
    
def test():
    ''' test your code thoroughly. put the testing cases here'''
    data={}
    with open(indexfile, "r") as read_file:
        data = json.load(read_file).items()
        for key,values in data:
            if(key.__contains__('barrier')):
                print("barrier occurs in ",values)
    with open(indexfile, "r") as read_file:
        data = json.load(read_file).keys()
    print("no of terms",len(data))
    with open("termfreqFile", "r") as read_file:
        freq_data = json.load(read_file).keys()
    print("no of terms",len(freq_data))
def indexingCranfield():
    #ToDo: indexing the Cranfield dataset and save the index to a file
    # command line usage: "python index.py cran.all index_file"
    # the index is saved to index_file
    coll={}
    collect= Collection()
    #creating object     
    invertindex=InvertedIndex() 
    
    #adding all documents to collection class
    for docu in cf.docs:
        coll={docu.docID:[docu.title,docu.author,docu.body]}
        collect.docs.update(coll)
        #invertindex.docs.update(coll)
    
    for docu in cf.docs:                 
        invertindex.indexDoc(docu)   
    
    #save to json file    
    invertindex.save(indexfile)
    # load from json file
    invertindex.load(indexfile)     
    
    
if __name__ == '__main__':
    
    #input cran file
    crfile =sys.argv[1]  
    #output index file 
    indexfile=sys.argv[2] 
    cf = CranFile (crfile)
    indexingCranfield()
    test()