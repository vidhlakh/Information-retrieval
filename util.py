
'''
   utility functions for processing terms

    shared by both indexing and query processing
'''
import nltk
#nltk.download(stopwords)
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

def isStopWord(word):
    ''' using the NLTK functions, return true/false'''
    st_words = set(stopwords.words("english"))
    #print(stop_words)
    #print(len(stop_words))
    if word in st_words:
        return True
    else:
        return False
   
    


def stemming(word):
    ''' return the stem, using a NLTK stemmer. check the project description for installing and using it'''
    porstem = PorterStemmer()
    return porstem.stem(word) 

'''word="Guessing"
t= isStopWord(word)
#print(t)
st=stemming(word)
print(st)'''