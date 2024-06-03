# docker run -d -p 8000:8000 --name dynamodb-local amazon/dynamodb-local

import boto3

# Create a DynamoDB client
dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')

# Create the table
table = dynamodb.create_table(
    TableName='TicketTable',
    KeySchema=[
        {
            'AttributeName': 'id',
            'KeyType': 'HASH'  # Partition key
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'id',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

# Wait until the table exists
table.meta.client.get_waiter('table_exists').wait(TableName='TicketTable')

print(f"Table {table.table_name} created successfully.")
