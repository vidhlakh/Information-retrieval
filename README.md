# Information-retrieval
Instructions to execute index.py
---------------------------------
Execution command: python index.py cran.all index_file
Number of terms will be printed
Index_file and termfreqfile having terms and term frequency are created
Instructions to execute query.py
---------------------------------
Execution command for boolean model:python query.py index_file 0 query.text 001
No of documents: 
Query Results

Execution command for vector model:python query.py index_file 1 query.text 001

Instructions to execute query.py
---------------------------------
Execution command: python batcheval.py index_file query.text qrels.text
