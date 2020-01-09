'''
a program for evaluating the quality of search algorithms using the vector model

it runs over all queries in query.text and get the top 10 results,
and then qrels.text is used to compute the NDCG metric

usage:
    python batch_eval.py index_file query.text qrels.text

    output is the average NDCG over all the queries

'''
import sys
import cranqry
def eval():
    qf = cranqry.loadCranQry (queryfile)
            
    

    print ('Done')

if __name__ == '__main__':
    #index file
    indexfile =sys.argv[1]  
    #query.text
    queryfile=sys.argv[2] 
    #qrelsfile
    qrelsfile=sys.argv[3]
    eval()
