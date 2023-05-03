import boto3

# Connects to the DynamoDB table and handles the query

def create_table(table_name="college"):
    return boto3.resource('dynamodb').Table(table_name)

def state_and_cost_range_query(table, state, low_cost, high_cost):
    query_params = {
        'KeyConditionExpression': 'statecode = :sc and cost between :minc and :maxc',
        'ExpressionAttributeValues': {':sc': state, ':minc': low_cost, ':maxc': high_cost }},
        'ProjectionExpression': 'statecode, city, instname, cost'
    response = table.query(**query_params)
    return response['Items']

#####################################
##  Testing only
  
def print_query_results(items):
    for item in items:
        print(f"{item['statecode']}, {item['city']}, {item['instname']}, {item['cost']}")
 
def test_query(state, low, high):
    print_query_results(state_and_cost_range_query(create_table(), state, low, high))
    



