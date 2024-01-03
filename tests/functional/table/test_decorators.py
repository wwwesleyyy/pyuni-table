def test_unique_decorator(table):
    @table.unique("email")
    class Example:
        email: str

    assert table.unique_indexes[Example.__name__] == {"email"}
