from moto import mock_dynamodb

from pyuni_table.table import Table


@mock_dynamodb
def test_table_create_table():
    table_name = 'test_table'
    table = Table(table_name)
    table.create_table()
    assert table.client.describe_table(TableName=table_name)['Table']['TableStatus'] == 'ACTIVE'


@mock_dynamodb
def test_table_delete_table():
    table_name = 'test_table'
    table = Table(table_name)
    table.create_table()
    table.delete_table()
    waiter = table.client.get_waiter('table_not_exists')
    waiter.wait(TableName=table_name)
    assert table.client.list_tables()['TableNames'] == []
