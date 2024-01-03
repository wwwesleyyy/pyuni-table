from collections import defaultdict, namedtuple
from typing import Callable, Type, TypeVar

import boto3

from pyuni_table.model import BaseModel

T = TypeVar("T", bound=BaseModel)

ItemTransitionSet = namedtuple(
    "ItemTransition",
    ["to_create", "to_delete", "to_update"],
    defaults=[set(), set(), set()],
)


class Table:
    """
    The primary interface to Pyuni Table.

    :param table: The name of the table in DynamoDB.
    :param region_name: The AWS region to use. If not specified, the default region will be used.
    """

    def __init__(self, table: str, region_name: str | None = None):
        self.name = table
        self.client = boto3.client("dynamodb", region_name=region_name)
        self.unique_indexes: dict[str, set[str]] = defaultdict(set)

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

    def unique(self, field: str) -> Callable:
        """
        Decorator to mark a field as unique.

        :param field: The field to mark as unique.
        """

        def decorator(cls):
            self.unique_indexes[cls.__name__].add(field)
            return cls

        return decorator

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

    def get(self, cls: Type[T], entity_id: str) -> T:
        """
        Get an entity from the table.

        :param cls: The type of the entity to get.
        :param entity_id: The ID of the entity to get.
        :return: The entity
        """
        response = self.client.get_item(
            TableName=self.name, Key={"pk": {"S": str(entity_id)}, "sk": {"S": "!"}}
        )
        return cls.model_validate_json(response["Item"]["data"]["S"])

    def graph(self, entity: BaseModel) -> set:
        """
        Transform an entity into a graph segment of items to be saved to DynamoDB.

        :param entity: The entity to transform.
        :return: A set of items to be saved to DynamoDB.
        """
        root_item = {
            "pk": {"S": str(entity.id)},
            "sk": {"S": "!"},
            "data": {"S": entity.model_dump_json()},
            "model": {"S": entity.__class__.__name__},
        }
        unique_items = set()
        for field in self.unique_indexes[entity.__class__.__name__]:
            item = {
                "pk": {
                    "S": f"unique##{entity.__class__.__name__}.{field}##{getattr(entity, field)}"
                },
                "sk": {"S": "!"},
                "model": {"S": entity.__class__.__name__},
            }
            unique_items.add(item)
        return {root_item, *unique_items}

    @staticmethod
    def diff(current: set, future: set) -> ItemTransitionSet:
        """
        Compare two sets of items and return the difference.

        :param current: The current set of items.
        :param future: The future set of items.
        :return: The difference between the two sets.
        """
        item_set = ItemTransitionSet(set(), set(), set())
        item_set.to_create = {
            f
            for f in future
            if (f["pk"], f["sk"]) not in [(c["pk"], c["sk"]) for c in current]
        }
        item_set.to_delete = {
            c
            for c in current
            if (c["pk"], c["sk"]) not in [(f["pk"], f["sk"]) for f in future]
        }
        item_set.to_update = {
            u
            for u in future
            if (u["pk"], u["sk"]) in [(c["pk"], c["sk"]) for c in current if c != u]
        }
        return item_set

    def build_transactions(
        self, item_set: ItemTransitionSet, current: BaseModel
    ) -> set:
        puts = [
            {"Put": {"TableName": self.name, "Item": entity}}
            for entity in item_set.to_create | item_set.to_update
        ]
        deletes = [
            {
                "Delete": {
                    "TableName": self.name,
                    "Key": {
                        "pk": entity["pk"],
                        "sk": entity["sk"],
                    },
                }
            }
            for entity in item_set.to_delete
        ]
        return set(puts + deletes)
