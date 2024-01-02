import boto3
import pytest
from moto import mock_dynamodb

from pyuni_table.table import Table


@pytest.fixture()
def client():
    return boto3.client('dynamodb', region_name='us-east-1')


@pytest.fixture()
def table_name():
    return 'test_table'


@pytest.fixture()
def table(table_name):
    with mock_dynamodb():
        table = Table(table_name, region_name='us-east-1')
        table.create_table()
        yield table
