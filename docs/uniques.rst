Unique Constraints
==================

Pyuni can enforce unique constraints on any field with a decorator.

.. code-block:: python

    from pyuni import BaseModel, Table

    table = Table('QuickStartTutorialTable', endpoint_url='http://localhost:8000')
    table.create_table()

    @table.unique('email')
    class User(BaseModel):
        name: str
        email: str
