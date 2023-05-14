import boto3

# Copied from console version

def create_table(table_name="document-titles"):
    return boto3.resource('dynamodb').Table(table_name)

def state_and_cost_range_query(table, id):
    query_params = {
        'KeyConditionExpression': 'id = :id',
        'ProjectionExpression': "id, title",
        'ExpressionAttributeValues': {':id': id} }
    response = table.query(**query_params)
    return response['Items']
    

#  Lambda-specific code
#  Convention is the handler is named lambda_handler and the file is named lambda_function

def lambda_handler(event, context):
    id = event['queryStringParameters']['id']
    items = state_and_cost_range_query(create_table(),id)
    return format_html_query_results(id, items)

# Generate a full HTML page from a list of items returned by the search
def format_html_query_results(id, items):
    banner_html = f"<h3>Search results for id {id}</h3><p/>"
    item_html = '<ol>'
    for item in items:
        item_html += f"<li>{item['id']}, {item['title']}</li>"
    item_html += '</ol>'
    html = f"<html><body>{banner_html} {item_html}</body></html>"    
    return {'statusCode': 200, 'headers': {'Content-Type': 'text/html'},'body': html}