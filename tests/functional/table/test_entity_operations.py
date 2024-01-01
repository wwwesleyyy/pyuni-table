from pyuni_table.model import BaseModel


def test_save(table, client):
    @table.model()
    class Example(BaseModel):
        str_field: str
        int_field: int

    example = Example(id='766f5f6a-dae5-47cf-9f75-033a6d257907', str_field='test', int_field=1)
    table.save(example)

    response = client.get_item(
        TableName=table.name,
        Key={
            'pk': {
                'S': str(example.id)
            },
            'sk': {
                'S': '!'
            }
        }
    )

    parsed_example = Example.model_validate_json(response['Item']['data']['S'])
    assert parsed_example == example


def test_get(table, client):
    @table.model()
    class Example(BaseModel):
        str_field: str
        int_field: int

    example = Example(id='766f5f6a-dae5-47cf-9f75-033a6d257907', str_field='test', int_field=1)

    client.put_item(
        TableName=table.name,
        Item={
            'pk': {
                'S': str(example.id)
            },
            'sk': {
                'S': '!'
            },
            'data': {
                'S': example.model_dump_json()
            },
            'model': {
                'S': example.__class__.__name__
            }
        }
    )

    result = table.get(example.id)
    assert result == example
