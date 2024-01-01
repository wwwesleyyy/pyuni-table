Quick Start
===========

.. warning::

    This library is still in early development and is not ready for
    production use.

Installation
------------

To use Pyuni Table, first install it using pip:

.. code-block:: console

    $ pip install pyuni-table

This tutorial assumes that you have DynamoDB running locally on port 8000.  AWS has a guide on `running DynamoDB
Locally <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html>`_.  Alternatively, you can
remove the ``endpoint_url`` parameter from the ``Table`` constructor and use the live AWS DynamoDB service with your
AWS credentials.

.. code-block:: python

    from pyuni import Table

    table = Table('QuickStartTutorialTable', endpoint_url='http://localhost:8000')
    table.create_table()

This creates your table with the necessary hash and sort keys and ``ttl`` field defined.

Working with Pydantic Models
----------------------------

Too keep things simple, Pyuni uses Pydantic models to marshall objects in and out of DynamoDB. The only requirement is
that models must have an ``id`` that can be cast to a ``str``, and that this ``id`` be unique across *all* of your
models, not just the model it's defined on.  For the sake of convenience, Pyuni offers a ``BaseModel`` that adds this
field for you.  Other than that, it's just a Pydantic ``BaseModel``.

.. code-block:: python

    from puni import BaseModel

    @table.model()
    class User(BaseModel):
        name: str
        email: str

Now we can save instances of the model directly to the table.

.. code-block:: python

    user = User(id='1', name='John Doe', email='john.doe@example.com')
    table.save(user)

And retrieve, update and destroy them.

.. code-block:: python

    user = table.get(1)

    user.name = 'Jane Doe'
    user.email = 'jane.doe@example.com'

    table.save(user)

    user = table.get(1)

    table.delete(user.id)

Once you're done, you can delete the table just as you'd expect.

.. code-block:: python

    table.delete_table()

