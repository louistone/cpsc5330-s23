import boto3

# Copied from console version

def create_table(table_name="term_fre"):
    return boto3.resource('dynamodb').Table(table_name)

def state_and_cost_range_query(table, term):
    query_params = {
        'KeyConditionExpression': 'term = :term',
        'ProjectionExpression': "term, fre, id",
        'ExpressionAttributeValues': {':term': term} }
    response = table.query(**query_params)
    return response['Items']
    

#  Lambda-specific code
#  Convention is the handler is named lambda_handler and the file is named lambda_function

def lambda_handler(event, context):
    term = event['queryStringParameters']['term']
    items = state_and_cost_range_query(create_table(),term)
    return format_html_query_results(id, items)

# Generate a full HTML page from a list of items returned by the search
def format_html_query_results(id, items):
    banner_html = f"<h3>Search results for id {id}</h3><p/>"
    item_html = '<ol>'
    for item in items:
        item_html += f"<li>{item['term']}, {item['fre']}, {item['id']}</li>"
    item_html += '</ol>'
    html = f"<html><body>{banner_html} {item_html}</body></html>"    
    return {'statusCode': 200, 'headers': {'Content-Type': 'text/html'},'body': html}