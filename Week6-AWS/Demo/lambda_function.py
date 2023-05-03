import boto3

# Copied from console version

def create_table(table_name="college"):
    return boto3.resource('dynamodb').Table(table_name)

def state_and_cost_range_query(table, state, low_cost, high_cost):
    query_params = {
        'KeyConditionExpression': 'statecode = :sc and cost between :minc and :maxc',
        'ProjectionExpression': "statecode, city, instname, cost",
        'ExpressionAttributeValues': {':sc': state, ':minc': low_cost, ':maxc': high_cost } }
    response = table.query(**query_params)
    return response['Items']
    

#  Lambda-specific code
#  Convention is the handler is named lambda_handler and the file is named lambda_function

def lambda_handler(event, context):
    statecode = event['queryStringParameters']['statecode']
    lowcost = int(event['queryStringParameters']['lowcost'])
    highcost = int(event['queryStringParameters']['highcost'])
    items = state_and_cost_range_query(create_table(),statecode, lowcost, highcost)
    return format_html_query_results(statecode, lowcost, highcost, items)

# Generate a full HTML page from a list of items returned by the search
def format_html_query_results(statecode, lowcost, highcost, items):
    banner_html = f"<h3>Search results for state {statecode}<br/>Low cost is {lowcost}<br/>High cost is {highcost}</h3><p/>"
    item_html = '<ol>'
    for item in items:
        item_html += f"<li>{item['city']}, {item['instname']}, {item['cost']}</li>"
    item_html += '</ol>'
    html = f"<html><body>{banner_html} {item_html}</body></html>"    
    return {'statusCode': 200, 'headers': {'Content-Type': 'text/html'},'body': html}







