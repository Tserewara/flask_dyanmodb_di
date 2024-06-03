import boto3
import pytest

from src.main import create_app
from src.ticket_repository import TicketRepositoryDynamoDB


def create_ticket_table(dynamo_client):
    table_name = "TicketTableTest"
    try:
        dynamo_client.meta.client.describe_table(TableName=table_name)
    except dynamo_client.meta.client.exceptions.ResourceNotFoundException:
        dynamo_client.create_table(
            TableName=table_name,
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
        dynamo_client.Table(table_name).meta.client.get_waiter('table_exists').wait(TableName=table_name)

        print("Table created successfully")


def delete_ticket_table(dynamo_client):
    table = dynamo_client.Table("TicketTableTest")
    table.delete()
    print("Table destroyed successfully")


@pytest.fixture
def dynamo_client():
    dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
    create_ticket_table(dynamodb)
    yield dynamodb
    delete_ticket_table(dynamodb)


@pytest.fixture
def app(dynamo_client):
    dependencies = {
        "ticket_repository": TicketRepositoryDynamoDB(dynamo_client, "TicketTableTest")
    }
    app = create_app(dependencies)

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def api_client(app):
    return app.test_client()


