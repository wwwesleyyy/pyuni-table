The Pyuni Table Documentation
=======================================

.. warning::

    This library is still in early development and is not ready for
    production use.

**Pyuni Table** is a Python library for storing, retrieving and indexing
`Pydantic <https://docs.pydantic.dev/latest/>`_ models in `DynamoDB <https://aws.amazon.com/pm/dynamodb/>`_. Pyuni
supports queries and unique constraints on any model field with a simple decorator. Relationships, too! Queries against
any index, relationship or aggregation can be done in a single trip to the database. And everything is stored in a
single table without the need for secondary indexes. Is there anything Pyuni can't support on DynamoDB? Yeah!
`Scan <https://dynobase.dev/dynamodb-scan/>`_.

Check out the :doc:`quick_start` section for some simple examples.

Contents
--------

.. toctree::
   quick_start
   uniques
   api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
