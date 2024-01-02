from typing import Type, TypeVar

import boto3

from pyuni_table.model import BaseModel

T = TypeVar("T", bound=BaseModel)


class Table:
    """
    The primary interface to Pyuni Table.

    :param table: The name of the table in DynamoDB.
    """

    def __init__(self, table: str, region_name: str | None = None):
        self.name = table
        self.client = boto3.client("dynamodb", region_name=region_name)

    def create_table(self) -> None:
        """
        Create a table in DynamoDB. The method will block until the table is available.
        """
        self.client.create_table(
            TableName=self.name,
            BillingMode="PAY_PER_REQUEST",
            AttributeDefinitions=[
                {"AttributeName": "pk", "AttributeType": "S"},
                {"AttributeName": "sk", "AttributeType": "S"},
            ],
            KeySchema=[
                {"AttributeName": "sk", "KeyType": "HASH"},
                {"AttributeName": "pk", "KeyType": "RANGE"},
            ],
        )
        waiter = self.client.get_waiter("table_exists")
        waiter.wait(TableName=self.name)
        self.client.update_time_to_live(
            TableName=self.name,
            TimeToLiveSpecification={"Enabled": True, "AttributeName": "ttl"},
        )

    def delete_table(self) -> None:
        """
        Delete a table in DynamoDB. The method will block until the table has been deleted.
        """
        self.client.delete_table(TableName=self.name)

    def save(self, entity: BaseModel) -> None:
        """
        Save an entity to the table.

        :param entity: The entity to save.
        """
        self.client.put_item(
            TableName=self.name,
            Item={
                "pk": {"S": str(entity.id)},
                "sk": {"S": "!"},
                "data": {"S": entity.model_dump_json()},
                "model": {"S": entity.__class__.__name__},
            },
            ReturnValues="NONE",
            ReturnConsumedCapacity="NONE",
            ReturnItemCollectionMetrics="NONE",
        )

        # DynamoDB.Client.exceptions.ConditionalCheckFailedException
        # DynamoDB.Client.exceptions.ProvisionedThroughputExceededException
        # DynamoDB.Client.exceptions.ResourceNotFoundException
        # DynamoDB.Client.exceptions.ItemCollectionSizeLimitExceededException
        # DynamoDB.Client.exceptions.TransactionConflictException
        # DynamoDB.Client.exceptions.RequestLimitExceeded
        # DynamoDB.Client.exceptions.InternalServerError

    def get(self, cls: Type[T], entity_id: str) -> T:
        response = self.client.get_item(
            TableName=self.name, Key={"pk": {"S": str(entity_id)}, "sk": {"S": "!"}}
        )
        return cls.model_validate_json(response["Item"]["data"]["S"])

        # DynamoDB.Client.exceptions.ConditionalCheckFailedException
        # DynamoDB.Client.exceptions.ProvisionedThroughputExceededException
        # DynamoDB.Client.exceptions.ResourceNotFoundException
        # DynamoDB.Client.exceptions.ItemCollectionSizeLimitExceededException
        # DynamoDB.Client.exceptions.TransactionConflictException
        # DynamoDB.Client.exceptions.RequestLimitExceeded
        # DynamoDB.Client.exceptions.InternalServerError
