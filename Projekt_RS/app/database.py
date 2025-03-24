import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000", region_name="eu-west-1")

def create_table_if_not_exists (table_name, key_schema, attribute_definitions):
    try:
        table = dynamodb.Table(table_name)
        table.meta.client.describe_table(TableName=table_name)
        print(f"Table {table_name} already exists")
    except ClientError as e:
        if e.response ["Error"]["Code"] == "ResourceNotFoundException":
            print(f"Creating talbe {table_name}...")
            table = dynamodb.create_table(
                TableName = table_name,
                KeySchema = key_schema,
                AttributeDefinitions = attribute_definitions,
                ProvisionedThroughput ={
                    "ReadCapacityUnits": 5,
                    "WriteCapacityUnits": 5
                }
            )
            table.meta.client.get_waiter("table_exists").wait(TableName=table_name)
            print(f"Table {table_name} created successfully")
        else:
            print (f"Unexpected error: {e}")

def create_tables():
    create_table_if_not_exists(
        "users",
        [{"AttributeName": "username", "KeyType": "HASH"}],
        [{"AttributeName": "username", "AttributeType": "S"}]
    )
    create_table_if_not_exists(
        "houses",
        [{"AttributeName": "houses_id", "KeyType": "HASH"}],
        [{"AttributeName": "houses_id", "AttributeType": "S"}]
    )
    create_table_if_not_exists(
        "comments",
        [{"AttributeName": "comment_id", "KeyType": "HASH"}],
        [{"AttributeName": "comment_id", "AttributeType": "S"}]
    )

create_tables()
users_table = dynamodb.Table('users') 