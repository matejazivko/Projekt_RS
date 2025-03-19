import boto3

dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8001", region_name="eu-west-1")

for table in dynamodb.tables.all():
    print(table.name)
