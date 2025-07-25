A streamlined Python library for MongoDB operations that prioritizes developer productivity and mental load reduction. mongo-helper wraps PyMongo with intuitive interfaces, automatic connection management, and convenient helper functions that eliminate boilerplate code common in MongoDB workflows. It also provides a simple way to build up [aggregation pipeline queries](https://www.mongodb.com/docs/manual/core/aggregation-pipeline).

The library is designed around the philosophy that database interactions should be simple, readable, and predictable. It provides both low-level control through the `Mongo` class and high-level convenience through the `Collection` wrapper, allowing developers to choose the appropriate abstraction level for their use case. mongo-helper integrates seamlessly with Docker-based development workflows and includes comprehensive query helpers for time-based data analysis.

This library is ideal for data engineers, analysts, and developers who work regularly with MongoDB and want to minimize the cognitive overhead of database operations while maintaining full access to MongoDB's capabilities. It fits naturally into data processing pipelines, analytics workflows, and rapid prototyping environments where developer velocity is crucial.

Tested for Python 3.5 - 3.13 against MongoDB 4.4 docker container.

Connect with a DB url in the following format:

- mongodb://someuser:somepassword@somehost:27017/admin

> See <https://docs.mongodb.com/manual/reference/connection-string> for connecting to a replica-set/cluster.
>
> Use percent encoding if your username or password includes `@`, `:`, `/`, or `%`.

## Install

```
pip install mongo-helper
```

## Configuration

mongo-helper uses a settings.ini file for Docker and connection configuration:

```ini
[default]
mongo_image_version = 4.4
mongo_username = mongouser
mongo_password = some.pass
query_db = db
use_none_cert = False
connect_timeout = 5
mongo_url =

[dev]
container_name = mongo-helper
port = 27017
rm = False
mongo_data_dir =
mongo_url = mongodb://mongouser:some.pass@localhost:27017/admin

[test]
container_name = mongo-helper-test
port = 27001
rm = True
mongo_data_dir =
mongo_url = mongodb://mongouser:some.pass@localhost:27001/admin
```

> On first use, the default settings.ini file is copied to `~/.config/mongo-helper/settings.ini`

## QuickStart

```python
import mongo_helper as mh

# Connect automatically using settings.ini configuration
mongo, total_docs = mh.connect_to_server()

# Use the high-level Collection wrapper for common operations
users = mh.Collection('users')

# Insert documents with minimal syntax
user_id = users.insert_one({'name': 'Alice', 'age': 30, 'status': 'active'})

# Query with convenient field selection
active_users = users.find({'status': 'active'}, fields='name, age', to_list=True)

# Count documents matching criteria
user_count = users.count({'age': {'$gte': 18}})

# Time-based queries using helper functions
recent_users = users.find(mh.get_days_ago_query(days_ago=7), to_list=True)

print(f"Found {len(active_users)} active users out of {user_count} total adults")
print(f"Recent signups: {len(recent_users)}")
```

This example demonstrates mongo-helper's key value propositions: automatic connection handling, simplified syntax for common operations, convenient field projection syntax, and time-based query helpers. You get MongoDB's full power with significantly less boilerplate code and mental overhead.

## API Overview

### Connection Management

**`connect_to_server(url=None, db=None, use_none_cert=None, attempt_docker=True, exception=False, show=False)`** - Connect to MongoDB server and return Mongo instance
- `url`: MongoDB connection URL, defaults to mongo_url from settings
- `db`: database name, defaults to query_db from settings
- `use_none_cert`: SSL certificate setting, defaults to use_none_cert from settings
- `attempt_docker`: if True, automatically start Docker container on connection failure
- `exception`: if True, raise exceptions on connection failure
- `show`: if True, display Docker commands and output
- Returns: tuple of (mongo_instance, total_documents_in_database) on success, (None, float('inf')) on failure
- Internal calls: `start_docker()`, `Mongo()`, `mongo.get_collections()`, `mongo.total_documents()`

**`start_docker(exception=False, show=False, force=False, wait=True, sleeptime=2)`** - Start MongoDB Docker container using settings.ini values
- `exception`: if True, raise exception on Docker errors
- `show`: if True, display Docker commands and output
- `force`: if True, stop and remove existing container before creating new one
- `wait`: if True, wait until MongoDB accepts connections
- `sleeptime`: seconds to sleep between connection checks when waiting
- Returns: result from bg_helper Docker functions
- Internal calls: `_settings_for_docker_ok()`, `bh.tools.docker_mongo_start()`

**`stop_docker(exception=False, show=False)`** - Stop MongoDB Docker container using settings.ini values
- `exception`: if True, raise exception on Docker errors
- `show`: if True, display Docker commands and output
- Returns: result from bg_helper Docker functions
- Internal calls: `_settings_for_docker_ok()`, `bh.tools.docker_stop()`

### High-Level Collection Interface

**`Collection(collection_name, mongo_instance=None, url=None, db=None, use_none_cert=None, attempt_docker=True, exception=True, show=False)`** - Convenient wrapper for MongoDB collection operations
- `collection_name`: name of MongoDB collection to work with
- `mongo_instance`: optional Mongo instance to use, creates one automatically if None
- `url`: MongoDB connection URL for automatic connection
- `db`: database name for automatic connection
- `use_none_cert`: SSL certificate setting for automatic connection
- `attempt_docker`: whether to attempt Docker startup for automatic connection
- `exception`: whether to raise exceptions for automatic connection
- `show`: whether to show output for automatic connection
- Internal calls: `mh.connect_to_server()`, `mongo.change_database()`

**`Collection.insert_one(document)`** - Add a document to the collection and return inserted_id
- `document`: dict of information to be inserted
- Returns: ObjectId of inserted document
- Internal calls: `mongo._insert_one()`

**`Collection.insert_many(documents)`** - Add several documents to the collection and return inserted_ids
- `documents`: list of dicts to insert
- Returns: list of ObjectIds for inserted documents
- Internal calls: `mongo._insert_many()`

**`Collection.find(query={}, fields='', ignore_fields='', to_list=False, **kwargs)`** - Return documents matching the query
- `query`: dict representing search criteria
- `fields`: string containing fields to return, separated by any of , ; |
- `ignore_fields`: string containing fields to ignore, separated by any of , ; |
- `to_list`: if True, return list instead of cursor
- `kwargs`: additional arguments passed to underlying _find method
- Returns: cursor or list of documents
- Internal calls: `mongo._find()`

**`Collection.find_one(query={}, fields='', ignore_fields='', **kwargs)`** - Return a single document matching the query
- `query`: dict representing search criteria
- `fields`: string containing fields to return, separated by any of , ; |
- `ignore_fields`: string containing fields to ignore, separated by any of , ; |
- `kwargs`: additional arguments passed to underlying _find_one method
- Returns: dict (single document) or string (if single field requested)
- Internal calls: `mongo._find_one()`

**`Collection.update_one(match, update, upsert=False)`** - Update one matching document and return number modified
- `match`: dict of query matching document to update
- `update`: dict of modifications to apply
- `upsert`: if True, perform insert if no documents match
- Returns: number of documents modified
- Internal calls: `mongo._update_one()`

**`Collection.update_many(match, update, upsert=False)`** - Update all matching documents and return number modified
- `match`: dict of query matching documents to update
- `update`: dict of modifications to apply
- `upsert`: if True, perform insert if no documents match
- Returns: number of documents modified
- Internal calls: `mongo._update_many()`

**`Collection.delete_one(match)`** - Delete one matching document and return number deleted
- `match`: dict of query matching document to delete
- Returns: number of documents deleted
- Internal calls: `mongo._delete_one()`

**`Collection.delete_many(match)`** - Delete all matching documents and return number deleted
- `match`: dict of query matching documents to delete
- Returns: number of documents deleted
- Internal calls: `mongo._delete_many()`

**`Collection.count(match={}, **kwargs)`** - Return count of documents matching criteria
- `match`: dict of query matching documents to count
- `kwargs`: additional arguments passed to underlying _count method
- Returns: integer count of matching documents
- Internal calls: `mongo._count()`

**`Collection.distinct(key, match={}, **kwargs)`** - Return list of distinct values for key among documents
- `key`: field name to get distinct values for
- `match`: dict of query matching documents
- `kwargs`: additional arguments passed to underlying _distinct method
- Returns: list of distinct values
- Internal calls: `mongo._distinct()`

**`Collection.bulk_write(operations, ordered=True, bypass_document_validation=False, debug=False)`** - Execute mixed write operations and return result
- `operations`: list of write operation objects (InsertOne, UpdateOne, UpdateMany, ReplaceOne, DeleteOne, DeleteMany)
- `ordered`: if True, execute in order and stop after first error
- `bypass_document_validation`: if True, bypass document validation
- `debug`: if True, drop into debugger on BulkWriteError
- Returns: BulkWriteResult object with operation information
- Internal calls: `mongo._bulk_write()`

### Low-Level Database Interface

**`Mongo(url=None, db=None, use_none_cert=None)`** - Instance that can execute MongoDB statements
- `url`: MongoDB connection URL, defaults to mongo_url from settings
- `db`: database name for queries, defaults to query_db from settings
- `use_none_cert`: if True, add "&ssl_cert_reqs=CERT_NONE" to URL for SSL connections
- Internal calls: `SETTINGS.get()`, `MongoClient()`

**`Mongo.get_databases(system=False)`** - Return list of database names
- `system`: if True, include system databases ('admin', 'config', 'local')
- Returns: list of database name strings
- Internal calls: `self._client.list_database_names()`

**`Mongo.get_collections(db=None)`** - Return list of collection names
- `db`: database name, uses current self._db if None
- Returns: list of collection name strings
- Internal calls: `self._client[db].list_collection_names()`

**`Mongo.change_database(db)`** - Set different database to use for queries
- `db`: database name to switch to
- Internal calls: sets `self._db`

**`Mongo.select_database(system=False)`** - Interactively select database to use for queries
- `system`: if True, include system databases in selection menu
- Internal calls: `ih.make_selections()`, `self.get_databases()`

### Database Statistics and Information

**`Mongo.db_stats(scale='bytes')`** - Return dict of database information
- `scale`: one of bytes, KB, MB, GB (note: avgObeSize always in bytes)
- Returns: dict with database statistics
- Internal calls: `self._command('dbStats')`

**`Mongo.coll_stats(collection, ignore_fields='wiredTiger, indexDetails', scale='bytes')`** - Return dict of collection information
- `collection`: collection name
- `ignore_fields`: string of output fields to ignore, separated by , ; |
- `scale`: one of bytes, KB, MB, GB (note: avgObeSize always in bytes)
- Returns: dict with collection statistics
- Internal calls: `self._command('collStats')`, `ih.ignore_keys()`

**`Collection.coll_stats(ignore_fields='wiredTiger, indexDetails', scale='bytes')`** - Return dict of collection information
- `ignore_fields`: string of output fields to ignore, separated by , ; |
- `scale`: one of bytes, KB, MB, GB (note: avgObeSize always in bytes)
- Returns: dict with collection statistics
- Internal calls: `mongo.coll_stats()`

**`Mongo.server_status(ignore_fields='wiredTiger, tcmalloc, metrics, logicalSessionRecordCache')`** - Return dict from serverStatus command
- `ignore_fields`: string of output fields to ignore, separated by , ; |
- Returns: dict with server status information
- Internal calls: `self._command('serverStatus')`, `ih.ignore_keys()`

**`Mongo.server_info(ignore_fields='buildEnvironment')`** - Return dict from client server_info
- `ignore_fields`: string of output fields to ignore, separated by , ; |
- Returns: dict with server information
- Internal calls: `self._client.server_info()`, `ih.ignore_keys()`

### Index Management

**`Collection.create_index(keys, unique=False, ttl=None, sparse=False, background=False, **kwargs)`** - Create index on collection
- `keys`: list of 2-item tuples with field name and direction (1 ascending, -1 descending)
- `unique`: if True, create uniqueness constraint
- `ttl`: time to live in seconds for documents
- `sparse`: if True, only index documents containing the indexed field
- `background`: if True, create index in background
- `kwargs`: additional arguments passed to underlying _create_index method
- Returns: index name
- Internal calls: `mongo._create_index()`

**`Collection.drop_index(name, **kwargs)`** - Drop index from collection
- `name`: name of index to drop
- `kwargs`: additional arguments passed to underlying method
- Internal calls: `mongo._drop_index()`

**`Collection.index_information()`** - Return dict of index information for collection
- Returns: dict with index information
- Internal calls: `mongo._index_information()`

**`Collection.index_names()`** - Return list of index names
- Returns: sorted list of index name strings
- Internal calls: `mongo._index_names()`

**`Collection.index_sizes(scale='bytes')`** - Return dict of index sizes
- `scale`: one of bytes, KB, MB, GB
- Returns: dict mapping index names to sizes
- Internal calls: `mongo._index_sizes()`

**`Collection.index_usage(name='', full=False)`** - Return index usage statistics
- `name`: name of specific index to check
- `full`: if True, return full list of dicts from $indexStats aggregation
- Returns: list of tuples or dicts with usage statistics
- Internal calls: `mongo._index_usage()`

### Time-Based Query Helpers

**`get_date_query(date_string, fmt='%Y-%m-%d', timezone="America/Chicago", timestamp_field='_id')`** - Return query dict for matching date in timezone
- `date_string`: date string to parse
- `fmt`: format the date_string is in
- `timezone`: timezone for determining start of day
- `timestamp_field`: name of timestamp field to query on
- Returns: dict with MongoDB query for the specified date
- Internal calls: `dh.date_start_utc()`, `ObjectId.from_datetime()`

**`get_days_ago_query(days_ago=0, until_days_ago=0, timezone="America/Chicago", timestamp_field='_id')`** - Return query dict for matching days ago in timezone
- `days_ago`: number of days ago to start from
- `until_days_ago`: number of days ago to end at
- `timezone`: timezone for day calculations
- `timestamp_field`: name of timestamp field to query on
- Returns: dict with MongoDB query for the specified day range
- Internal calls: `dh.days_ago()`, `ObjectId.from_datetime()`

**`get_hours_ago_query(hours_ago=1, until_hours_ago=0, timestamp_field='_id')`** - Return query dict for matching hours ago
- `hours_ago`: number of hours ago to start from
- `until_hours_ago`: number of hours ago to end at
- `timestamp_field`: name of timestamp field to query on
- Returns: dict with MongoDB query for the specified hour range
- Internal calls: `dh.utc_now_localized()`, `dh.timedelta()`, `ObjectId.from_datetime()`

**`get_minutes_ago_query(minutes_ago=1, until_minutes_ago=0, timestamp_field='_id')`** - Return query dict for matching minutes ago
- `minutes_ago`: number of minutes ago to start from
- `until_minutes_ago`: number of minutes ago to end at
- `timestamp_field`: name of timestamp field to query on
- Returns: dict with MongoDB query for the specified minute range
- Internal calls: `dh.utc_now_localized()`, `dh.timedelta()`, `ObjectId.from_datetime()`

### Utility Methods

**`Collection.first_obj(match={}, timestamp_field='_id', fields='', ignore_fields='', **kwargs)`** - Return first object in collection
- `match`: query criteria passed to _find_one
- `timestamp_field`: name of timestamp field to sort on
- `fields`: string of fields to return, separated by , ; |
- `ignore_fields`: string of fields to ignore, separated by , ; |
- `kwargs`: additional arguments passed to underlying method
- Returns: dict with first document
- Internal calls: `mongo.first_obj()`

**`Collection.last_obj(match={}, timestamp_field='_id', fields='', ignore_fields='', **kwargs)`** - Return last object in collection
- `match`: query criteria passed to _find_one
- `timestamp_field`: name of timestamp field to sort on
- `fields`: string of fields to return, separated by , ; |
- `ignore_fields`: string of fields to ignore, separated by , ; |
- `kwargs`: additional arguments passed to underlying method
- Returns: dict with last document
- Internal calls: `mongo.last_obj()`

**`Collection.obj_id_set(match)`** - Return set of ObjectIds for matching documents
- `match`: dictionary representing documents to match
- Returns: set of ObjectId values
- Internal calls: `mongo.obj_id_set()`

**`Collection.total_documents()`** - Return total count of documents in collection
- Returns: integer count using estimated_document_count
- Internal calls: `mongo.total_documents()`

### Advanced Operations

**`Mongo._build_pipeline(match=None, group_by=None, timestamp_field='_id', unwind=None, include_array_index=False, projection=None, limit=None, to_set=None, to_list=None, to_sum=None, out=None)`** - Build aggregation pipeline
- `match`: dictionary for match stage
- `group_by`: list of keys to group by or string separated by , ; |
- `timestamp_field`: timestamp field name for sorting when limit specified
- `unwind`: list of keys to unwind or string separated by , ; |
- `include_array_index`: if True, include array index in unwind operations
- `projection`: list of keys to project or string separated by , ; |
- `limit`: maximum number of items
- `to_set`: keys to add to set for each group or string separated by , ; |
- `to_list`: keys to add to list for each group or string separated by , ; |
- `to_sum`: keys to sum for each group or string separated by , ; |
- `out`: collection name to save results to
- Returns: list of pipeline stages for aggregation
- Internal calls: `ih.get_list_from_arg_strings()`

**`Mongo.ez_pipeline(collection, match, group_by, timestamp_field='_id', unwind=None, include_array_index=False, projection=None, limit=None, to_set=None, to_list=None, to_sum=None, group_action=None, include_condition=None, verbose=False)`** - Build/run aggregation pipeline to group and count data
- `collection`: collection name
- `match`: dictionary for match stage
- `group_by`: list of keys to group by or string separated by , ; |
- `timestamp_field`: timestamp field for sorting
- `unwind`: keys to unwind or string separated by , ; |
- `include_array_index`: if True, include array index in unwind
- `projection`: keys to project or string separated by , ; |
- `limit`: maximum items
- `to_set`: keys to add to set or string separated by , ; |
- `to_list`: keys to add to list or string separated by , ; |
- `to_sum`: keys to sum or string separated by , ; |
- `group_action`: callable mapped over each grouped item
- `include_condition`: callable returning bool for item inclusion
- `verbose`: if True, print generated pipeline
- Returns: dict with keys 'counts', 'data', 'total', 'group_by', 'duration', 'pipeline', 'total_percent'
- Internal calls: `self._build_pipeline()`, `self._aggregate()`, `dh.utc_now_localized()`
