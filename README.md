# PyuniTable

> [!WARNING]
> This library is still in early development and is not ready for production use.

Pyuni Table is a Python library for storing, retrieving and indexing Pydantic models in DynamoDB. Pyuni supports
queries and unique constraints on any model field with a simple decorator. Relationships, too! Queries against any
index, relationship or aggregation can be done in a single trip to the database. And everything is stored in a single
table without the need for secondary indexes. Is there anything Pyuni can’t support on DynamoDB? Yeah! Scan.
