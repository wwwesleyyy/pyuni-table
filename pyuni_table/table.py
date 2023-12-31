import boto3


class Table:
    """
    The primary interface to Pyuni Table.

    :param table: The name of the table in DynamoDB.
    """

    def __init__(self, table: str):
        self.name = table
        self.client = boto3.client('dynamodb')

    def create_table(self) -> None:
        """
        Create a table in DynamoDB. The method will block until the table is available.
        """
        self.client.create_table(
            TableName=self.name,
            BillingMode='PAY_PER_REQUEST',
            AttributeDefinitions=[
                {
                    'AttributeName': 'pk',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'sk',
                    'AttributeType': 'S'
                },
            ],
            KeySchema=[
                {
                    'AttributeName': 'sk',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'pk',
                    'KeyType': 'RANGE'
                },
            ],
        )
        waiter = self.client.get_waiter('table_exists')
        waiter.wait(TableName=self.name)
        self.client.update_time_to_live(
            TableName=self.name,
            TimeToLiveSpecification={
                'Enabled': True,
                'AttributeName': 'ttl'
            }
        )

    def delete_table(self) -> None:
        """
        Delete a table in DynamoDB. The method will block until the table has been deleted.
        """
        self.client.delete_table(TableName=self.name)

    def save(self, entity: dict) -> None:
        """
        Save an entity to the table.

        :param entity: The entity to save.
        """
        pass
