import boto3
import termify

###############################################
#  Entry point is a function search(line) where line is the 
#    input query.  Output is a sequence of the form (docname, relevance) of 
#    length at most 5, and sorted in descending order of relevance

#  Step 1 -- Make connections to the two dynamodb tables
def create_docid_table(table_name="doctitles"):
    return boto3.resource('dynamodb').Table(table_name)

def create_tfidf_table(table_name="tfidf"):
    return boto3.resource('dynamodb').Table(table_name)

docid_table = create_docid_table();
tfidf_table = create_tfidf_table();

###################################################
# get_docids_for_terms
# Input is a sequence of terms.  Output is a set of docids -- the set of 
#  all docids that contain one or more of the terms
def get_docids_for_terms(terms):
    docids = set()
    for term in terms:
        #  Make dynamodb call to get all docids for that term, and add them to the set
        query_params = {
            'KeyConditionExpression': 'term = :term',
            'ProjectionExpression': "term,id",
            'ExpressionAttributeValues': {':term': term} }
        response = tfidf_table.query(**query_params)
        items = response['Items']
        for item in items:
            docids.add(item['id'])
    return docids

# get_tfidf
#  Input is a term and docid, output is the stored TF-IDF value for
#  that pair, or 0.0 if there is no stored value
def get_tfidf(term, docid):
    query_params = {
        'KeyConditionExpression': 'term = :term and id = :docid',
        'ProjectionExpression': "term, id, fre",
        'ExpressionAttributeValues': {':term': term,':docid': docid} }
    response = tfidf_table.query(**query_params)
    items = response['Items']
    if items:
        return items[0]['fre']
    else:
        return 0.0
  
# get_doc_title
#   Input is a docid, output is the stored name (title) for the document as stored in Dynamodb, or None if 
#     there is no such entry
def get_doc_title(docid):
    query_params = {
        'KeyConditionExpression': 'id = :id',
        'ProjectionExpression': "id, title",
        'ExpressionAttributeValues': {':id': docid}}
    response = docid_table.query(**query_params)
    items = response['Items']
    if items:
        return items[0]['title']
    else:
        return None
##########################################################

def search(line):
    terms = termify.termify(line)
    docids = get_docids_for_terms(terms)
    return sort_and_limit([(docid, compute_doc_relevance(docid, terms)) for docid in docids])

##  Implements the formula for relevance specified in the assignment -- output is a float.
##    Should return 0.0 if the terms list is empty or none of the terms appear in the document   

def compute_doc_relevance(docid, terms):
    pass
   
## Input pairs are (docid, tfidf)
##    Sort in descending order of tfidf, choose the top five, 
##    retrieve the doc title, and truncate tfidf to an integer
##    Output is a list of at most 5 pairs of the form (docname, int-tfidf)
   
def sort_and_limit(pairs):
    pass
