import boto3

# Copied from console version

def create_table(table_name="tfidf"):
    return boto3.resource('dynamodb').Table(table_name)

tfidf_table = create_table()

def get_tfidf(term, docid):
    query_params = {
        'KeyConditionExpression': 'term = :term and id = :docid',
        'ProjectionExpression': "term, id, fre",
        'ExpressionAttributeValues': {':term': term,':docid': docid} }
    response = tfidf_table.query(**query_params)
    items = response['Items']
    if items:
        print(items)
        return items[0]['fre']
    else:
        return 0.0
        
#  Lambda-specific code
#  Convention is the handler is named lambda_handler and the file is named lambda_function

def lambda_handler(event, context):
    term = event['queryStringParameters']['term']
    #items = state_and_cost_range_query(create_table(),term)
    docid = event['queryStringParameters']['docid']
    tfidf = get_tfidf(term, docid)
    return format_html_query_results(term,docid,tfidf)

# Generate a full HTML page from a list of items returned by the search
def format_html_query_results(term,docid,tfidf):
    banner_html = f"<h3>Search results for term {term} and docid {docid}</h3><p/>"
    item_html = f"<h3>tfidf {tfidf}</h3><p/>"
    # item_html = '<ol>'
    # for item in items:
    #     item_html += f"<li>{item['term']}, {item['fre']}, {item['id']}</li>"
    # item_html += '</ol>'
    html = f"<html><body>{banner_html} {item_html}</body></html>"    
    return {'statusCode': 200, 'headers': {'Content-Type': 'text/html'},'body': html}