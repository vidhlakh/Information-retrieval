'''
query processing

'''

import norvig_spell
import sys
import json
from util import isStopWord
from util import stemming
from nltk.tokenize import RegexpTokenizer
from index import IndexItem
from index import Posting
from index import InvertedIndex
from cranqry import loadCranQry
from doc import Collection
from doc import Document
import numpy as np
from functools import reduce
import math
import cran
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
class QueryProcessor:

    def __init__(self, query_text, index_data, collectionofdocs):
        ''' index is the inverted index; collection is the document collection'''
        self.raw_query = query_text
        self.index = index_data
        self.docs = collectionofdocs
        self.q_tf_dino=0     
        
    def preprocessing(self):
        
        
        tokenizer = RegexpTokenizer(r'\w+')
        querytokens = tokenizer.tokenize(self.raw_query)
        self.q_tf_dino=len(querytokens)   #length of the query
        #make spell correction
        for counter,querytoken in enumerate(querytokens):
            
            querytokens[counter] = norvig_spell.correction(querytoken)
            
        #replace the token after stemming        
        for counter,querytoken in enumerate(querytokens):
            stemmed_term = stemming(querytoken)
            querytokens[counter]=stemmed_term  
            #remove stop words from token
            token_is_stopword=isStopWord(querytoken)
            if(token_is_stopword):
                querytokens.pop(counter)
            
        print("Query tokens", querytokens)    
        return querytokens


    def booleanQuery(self,querytokens):
        ''' boolean query processing; note that a query like "A B C" is transformed to "A AND B AND C" for retrieving posting lists and merge them'''
        #ToDo: return a list of docIDs
        result = []
        intersect_results=[]
        for querytoken in querytokens:
            for key, value in self.index:
                for k,v in value.items():
                    if(key.__contains__(querytoken)):
                        result.append(k)
                    intersect_results.append(result)    
        docids=reduce(np.intersect1d,intersect_results)
        print("Number of Documents:",len(docids))
        
        return docids


    def vectorQuery(self,querytokens):
        ''' vector query processing, using the cosine similarity. '''
        #ToDo: return top k pairs of (docID, similarity), ranked by their cosine similarity with the query in the descending order
        # You can use term frequency or TFIDF to construct the vectors
        
        k=3
        No_docu=1400
        query={}
        
        with open("termfreqFile", "r") as read_file:
            freq_data = json.load(read_file).items()
        query_vectors=pd.DataFrame()
        
        docu_vectors=pd.DataFrame()
        cos_sim=pd.DataFrame()
        tf=0
        #construct Query vector
        for querytoken in querytokens:
            
            if(query.__contains__(querytoken)):
                tf+=1/self.q_tf_dino
                query[querytoken].update(tf)
            else:
                tf=1/self.q_tf_dino
                query.update({querytoken:tf})
        for querytoken in querytokens:
            q_tf=[]
            q_tf_idf=[] 
            q_df=1
            for key,value in freq_data:
                if(key.__contains__(querytoken)):
                    for k,v in value.items():
                        q_df=len(k)
            for key,value in query.items():
                if(key.__contains__(querytoken)):
                    
                    q_tf.append(value)
                    
            
            q_idf=math.log10(No_docu/q_df)
            
            for count,q_tff in enumerate(q_tf):
                q_tf_idf.append((math.log10(1+q_tff))+q_idf)
            temp=pd.DataFrame(q_tf_idf)
            query_vectors=pd.concat([query_vectors,temp])
        print("Query vectors for query 001",query_vectors)
        
        #Construct Document vector        
        for querytoken in querytokens:
            tf=[]
            tf_idf=[]  
            
            df=1
            
            for key,value in freq_data:
                if(key.__contains__(querytoken)):
                    for k,v in value.items():
                        
                        tf.append(v)
                        df=len(k)
        
                            
            
            
            idf=math.log10(No_docu/df)
           
            for tff in tf:
                tf_idf.append((math.log10(1+tff))*idf)
            docu_vector= pd.DataFrame(tf_idf)
            docu_vectors=pd.concat([docu_vectors,docu_vector])
            
        #cosine similarity   
        cos_sim=cosine_similarity(query_vectors, docu_vectors)
        print(cos_sim[1:4])
def test():
    ''' test your code thoroughly. put the testing cases here'''
    
        
    print ('Pass')

def query():
    ''' the main query processing program, using QueryProcessor'''

    # ToDo: the commandline usage: "echo query_string | python query.py index_file processing_algorithm"
    # processing_algorithm: 0 for booleanQuery and 1 for vectorQuery
    # for booleanQuery, the program will print the total number of documents and the list of docuement IDs
    # for vectorQuery, the program will output the top 3 most similar documents
    
    index_data={}    
   
    collect=Collection()
  
    qf = loadCranQry (query_doc)
    for q in qf:
        if (qf[q].qid == query_id):
            query_text = qf[q].text
    
    # loading index_file
    with open(index_file, "r") as read_file:
        index_data = json.load(read_file).items()
            
   
    queryprocess = QueryProcessor(query_text, index_data, collect.docs )
            
    
    querytokens=queryprocess.preprocessing()
    print("process alg:",process_alg)
    if(process_alg=='0'):
        result= queryprocess.booleanQuery(querytokens)
        print("Query results",result)
    elif(process_alg=='1'):
        result= queryprocess.vectorQuery(querytokens)
    else:
        print("enter 0 for boolean query and 1 for vector query")
    
    
        
        
    
if __name__ == '__main__':
    #test()
    #index file
    index_file = sys.argv[1]  
    process_alg=sys.argv[2]
    #query document
    query_doc=sys.argv[3]
    #query id
    query_id = sys.argv[4]
    
    query()
