from pyuni_table.model import BaseModel


def test_model(table):
    @table.model()
    class Example(BaseModel):
        str_field: str
        int_field: int

    assert table.models == {'Example': Example}
