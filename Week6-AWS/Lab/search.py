import boto3
import re

stopwords = set(["a", "as", "able", "about", "above", "according", "accordingly",
	     "across", "actually", "after", "afterwards", "again", "against", "aint", "all", "allow",
	     "allows", "almost", "alone", "along", "already", "also", "although", "always", "am", "among",
	     "amongst", "an", "and", "another", "any", "anybody", "anyhow", "anyone", "anything", "anyway",
	     "anyways", "anywhere", "apart", "appear","appreciate", "appropriate", "are", "arent", "around",
	     "as", "aside", "ask", "asking", "associated", "at", "available", "away", "awfully", "be", "became",
	     "because", "become", "becomes", "becoming", "been", "before", "beforehand", "behind",
	     "being", "believe", "below", "beside", "besides", "best", "better", "between", "beyond",
	     "both", "brief", "but", "by", "cmon", "cs", "came", "can", "cant", "cannot", "cant",
	     "cause", "causes", "certain", "certainly", "changes", "clearly", "co", "com", "come",
	     "comes", "concerning", "consequently", "consider", "considering", "contain", "containing",
	     "contains", "corresponding", "could", "couldnt", "course", "currently", "definitely",
	     "described", "despite", "did", "didnt", "different", "do", "does", "doesnt", "doing",
	     "dont", "done", "down", "downwards", "during", "each", "edu", "eg", "eight", "either",
	     "else", "elsewhere", "enough", "entirely", "especially", "et", "etc", "even", "ever",
	     "every", "everybody", "everyone", "everything", "everywhere", "ex", "exactly", "example",
	     "except", "far", "few", "ff", "fifth", "first", "five", "followed", "following", "follows",
	     "for", "former", "formerly", "forth", "four", "from", "further", "furthermore", "get",
	     "gets", "getting", "given", "gives", "go", "goes", "going", "gone", "got", "gotten",
	     "greetings", "had", "hadnt", "happens", "hardly", "has", "hasnt", "have", "havent",
	     "having", "he", "hes", "hello", "help", "hence", "her", "here", "heres", "hereafter",
	     "hereby", "herein", "hereupon", "hers", "herself", "hi", "him", "himself",
	     "his", "hither", "hopefully", "how", "howbeit", "however", "i", "id", "ill", "im", "ive",
	     "ie", "if", "ignored", "immediate", "in", "inasmuch", "inc", "indeed", "indicate",
	     "indicated", "indicates", "inner", "insofar", "instead", "into", "inward", "is",
	     "isnt", "it", "itd", "itll", "its", "its", "itself", "just", "keep", "keeps", "kept",
	     "know", "knows", "known", "last", "lately", "later", "latter", "latterly", "least",
	     "less", "lest", "let", "lets", "like", "liked", "likely", "little", "look", "looking",
	     "looks", "ltd", "mainly", "many", "may", "maybe", "me", "mean", "meanwhile", "merely",
	     "might", "more", "moreover", "most", "mostly", "much", "must", "my", "myself",
	     "name", "namely", "nd", "near", "nearly", "necessary", "need", "needs", "neither",
	     "never", "nevertheless", "new", "next", "nine", "no", "nobody", "non", "none", "noone",
	     "nor", "normally", "not", "nothing", "novel", "now", "nowhere", "obviously", "of",
	     "off", "often", "oh", "ok", "okay", "old", "on", "once", "one", "ones", "only",
	     "onto", "or", "other", "others", "otherwise", "ought", "our", "ours", "ourselves",
	     "out", "outside", "over", "overall", "own", "particular", "particularly",
	     "per", "perhaps", "placed", "please", "plus", "possible", "presumably", "probably",
	     "provides", "que", "quite", "qv", "rather", "rd", "re", "really", "reasonably",
	     "regarding", "regardless", "regards", "relatively", "respectively", "right", "said",
	     "same", "saw", "say", "saying", "says", "second", "secondly", "see", "seeing",
	     "seem", "seemed", "seeming", "seems", "seen", "self", "selves", "sensible", "sent",
	     "serious", "seriously", "seven", "several", "shall", "she", "should", "shouldnt",
	     "since", "six", "so", "some", "somebody", "somehow", "someone", "something",
	     "sometime", "sometimes", "somewhat", "somewhere", "soon", "sorry", "specified", "specify",
	     "specifying", "still", "sub", "such", "sup", "sure", "ts", "take", "taken", "tell", "tends",
	     "th", "than", "thank", "thanks", "thanx", "that", "thats", "thats", "the", "their", "theirs",
	     "them", "themselves", "then", "thence", "there", "theres", "thereafter", "thereby",
	     "therefore", "therein", "theres", "thereupon", "these", "they", "theyd",
	     "theyll", "theyre", "theyve", "think", "third", "this", "thorough",
	     "thoroughly", "those", "though", "three", "through", "throughout", "thru",
	     "thus", "to", "together", "too", "took", "toward", "towards", "tried", "tries",
	     "truly", "try", "trying", "twice", "two", "un", "under", "unfortunately",
	     "unless", "unlikely", "until", "unto", "up", "upon", "us", "use", "used",
	     "useful", "uses", "using", "usually", "value", "various", "very", "via", "viz",
	     "vs", "want", "wants", "was", "wasnt", "way", "we", "wed", "well", "were", "weve",
	     "welcome", "well", "went", "were", "werent", "what", "whats", "whatever", "when",
	     "whence", "whenever", "where", "wheres", "whereafter", "whereas", "whereby",
	     "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who",
	     "whos", "whoever", "whole", "whom", "whose", "why", "will", "willing", "wish",
	     "with", "within", "without", "wont", "wonder", "would", "would", "wouldnt", "yes",
	     "yet", "you", "youd", "youll", "youre", "youve", "your", "yours", "yourself",
	     "yourselves", "zero"])

def termify(line):
    terms = []
    words = re.findall(r'[^\W_]+', line)
    for word in words:
        lowered = word.lower()
        if (len(lowered) > 1) and (lowered not in stopwords) and (not re.search(r'^\d*$', lowered)):
            terms.append(lowered)
    return terms

###############################################
#  Entry point is a function search(line) where line is the 
#    input query.  Output is a sequence of the form (docname, relevance) of 
#    length at most 5, and sorted in descending order of relevance

#  Step 1 -- Make connections to the two dynamodb tables
def create_docid_table(table_name="doctitles"):
    return boto3.resource('dynamodb').Table(table_name)

def create_tfidf_table(table_name="tfidf3"):
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
        return float(items[0]['fre'])
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
    terms = termify(line)
    docids = get_docids_for_terms(terms)
    return sort_and_limit([(docid, compute_doc_relevance(docid, terms)) for docid in docids])

##  Implements the formula for relevance specified in the assignment -- output is a float.
##    Should return 0.0 if the terms list is empty or none of the terms appear in the document   
def compute_doc_relevance(docid, terms):
    total = 0.0
    for term in terms:
        total = total + get_tfidf(term, docid)
    return total/(len(terms)*1.0)
## Input pairs are (docid, tfidf)
##    Sort in descending order of tfidf, choose the top five, 
##    retrieve the doc title, and truncate tfidf to an integer
##    Output is a list of at most 5 pairs of the form (docname, int-tfidf)

def sort_and_limit(pairs):
    sorted_pairs = sorted(pairs, key=lambda x: x[1], reverse=True)
    top_5_pairs = sorted_pairs[:5]
    
    processed_pairs = []
    for pair in top_5_pairs:
        docid = pair[0]
        relevance = int(pair[1])
        title = get_doc_title(docid)
        processed_pairs.append((title, relevance))
    
    return processed_pairs

def lambda_handler(event, context):
    line = event['queryStringParameters']['line']
    results = search(line)
    return format_html_query_results(line,results)

# Generate a full HTML page from a list of items returned by the search
def format_html_query_results(line,results):
    banner_html = f"<h3>Search results for:{line}</h3><p/>"
    item_html = '<ol>'
    for result in results:
        item_html += f"<li>{result[0]} -- {result[1]}</li>"
    item_html += '</ol>'
    html = f"<html><body>{banner_html}{item_html}</body></html>"   
    return {'statusCode': 200, 'headers': {'Content-Type': 'text/html'},'body': html}
