This package wraps the pymongo driver for MongoDB.

When this package was initially created in 2019, one of the big priorities was
providing a simple way to build up [aggregation pipeline
queries](https://www.mongodb.com/docs/manual/core/aggregation-pipeline) in
MongoDB version 4.4 (a replacement to the original map-reduce functionality in
older versions of MongoDB). This is accomplished via the `_build_pipeline`
method.

There is an `ez_pipeline` method that uses the `_build_pipeline` result to
execute the aggregation pipeline query, then **group and count the results in a
manner suitable for rendering into live reports** in a web app.

### Sept 2024 Note

> The last release (v0.0.13) was on 1/20/20. At the time, there were a handful
> of features I wanted to add before I updated the README to showcase usage
> examples and let people know this project was worth using. Obviously that
> hasn't happened yet.
>
> Most of the wrapper methods to basic operations on MongoDB collections are
> prefixed with a `_` (which usually means you shouldn't use them directly).
> These include `_insert_one`, `_insert_many`, `_update_one`, `_update_many`,
> `_delete_one`, `_delete_many`, `_find`, `_find_one`, `_distinct`, `_count`,
> `_aggregate`, `_create_index`, `_drop_index`, `_drop_indexes`,
> `_drop_collection`, `_index_information`, `_index_names`, `_index_sizes`,
> `_index_usage`, `_build_pipeline`, `_explain_pipeline`, and `_explain_cursor`.
>
> There is not currently a wrapper to `bulk_write` (which lets you pass in a
> list of operations `InsertOne`, `UpdateOne`, `UpdateMany`, `ReplaceOne`,
> `DeleteOne`, or `DeleteMany`).

## Install

```
$ pip3 install mongo-helper
```

### Sept 2024 Note

> At the moment, there is an issue when using a version of Python greater than
> 3.9 with this package.

```
ServerSelectionTimeoutError: PY_SSIZE_T_CLEAN macro must be defined for '#' formats
```

> The version of pymongo currently pinned to this package is 3.7.2. It's
> possible that a newer version of pymongo has resolved this, but I **will not
> adjust the pinned version in this package until I've added docs and pytest
> tests for the existing features** in multiple versions of Python for multiple
> versions of MongoDB server.

You can use <https://github.com/pyenv/pyenv> to install Python 3.9 locally.

## Usage

### Starting a database container with docker

Since [bg-helper](https://pypi.org/project/bg-helper) is included in this
package, you can use the `docker_mongo_start` function to start or create a
mongo container (if your system has docker installed and your user has
permission to use it). See the [bg-helper docker
tools](https://github.com/kenjyco/bg-helper/blob/master/bg_helper/tools/_docker.py)
for more info.

```
import bg_helper as bh

bh.tools.docker_mongo_start('some-mongo-container')
```

> You can pass in a `version` (defaults to '4.4'), a port (defaults to 27000), a
> `username` (defaults to `mongouser`), a `password` (defaults to `some.pass`),
> and a `data_dir` (defaults to None).

### Connecting to a database

Import `mongo_helper` and create an instance of the `Mongo` class from your
connection string.

> See <https://docs.mongodb.com/manual/reference/connection-string> for
> connecting to a replica-set/cluster.
>
> Use percent encoding if your username or password includes `@`, `:`, `/`, or
> `%`.

```
import mongo_helper as mh


mongo = mh.Mongo(
    url='mongodb://someuser:somepassword@somehost:27017/admin',
    db='some_db'
)
```

### Connecting to a database when using a settings.ini file

If you have a `settings.ini` file, use
[settings-helper](https://pypi.org/project/settings-helper) to get your
connection string and database name.

```
[default]
mongo_url = mongodb://mongouser:some.pass@localhost:27000/admin
mongo_db_name = some_db
```

```
import mongo_helper as mh
import settings_helper as sh


settings = sh.get_all_settings().get('default')
mongo = mh.Mongo(
    url=settings['mongo_url'],
    db=settings['mongo_db_name']
)
```

> As long as the variables are defined in the settings.ini file, you can set
> environment variables to load the values. Environment variables that have the
> same name as variables defined in the settings.ini (or their UPPERCASE
> variant) will always override what is in the settings.ini file.

```
[default]
mongo_url =
mongo_db_name =
```

```
MONGO_URL="..." MONGO_DB_NAME="..." venv/bin/python your_script.py
```

### Adding data

You can use the `_insert_one` method to add a dict to a collection.

```
mongo._insert_one(collection_name, some_dict)
```

You can use the `_insert_many` method to add a list of dicts to a collection.

```
mongo._insert_many(collection_name, list_of_dicts)
```

or

```
try:
    mongo._insert_many(collection_name, list_of_dicts)
except Exception as e:
    for some_dict in list_of_dicts:
        try:
            mongo._insert_one(collection_name, some_dict)
        except Exception as e2:
            logger.error(e2)
            # Maybe start a pdb debugging session
            raise
```

You can use the `_update_one` method (with `upsert=True`) to add a dict to a
collection if it is not already there.

```
match_query = {
    'some_field': some_value,
    'some_other_field': some_other_value,
}
update_statement = {'$set': some_dict}
mongo._update_one(
    collection_name,
    match_query,
    update_statement,
    upsert=True
)
```

### Getting basic stats

You can call the `db_stats`, `coll_stats`, or `server_info` methods to get some
basic info about your database and collections.

```
print('mongo.db_stats():')
pprint(mongo.db_stats())
print('\nmongo.server_info():')
pprint(mongo.server_info())
```

```
pprint(mongo.coll_stats(collection_name))
```

### Updating data

.

### Finding data

.

### Building and executing "aggregation pipeline queries"

.

## Resources

### Official MongoDB

- <https://docs.mongodb.com/manual/reference/connection-string/>
- <http://api.mongodb.com/python/current/tutorial.html>
- <https://api.mongodb.com/python/current/api/pymongo/collection.html>
- <https://docs.mongodb.com/manual/indexes/>
- <https://api.mongodb.com/python/current/api/index.html>
- <https://api.mongodb.com/python/current/examples/index.html>
- <https://api.mongodb.com/python/current/examples/bulk.html>
- <https://docs.mongodb.com/manual/tutorial/create-indexes-to-support-queries/>
- <https://docs.mongodb.com/manual/tutorial/sort-results-with-indexes/>
- <https://www.mongodb.com/docs/manual/core/aggregation-pipeline>

### PyMongo driver

- <https://pymongo.readthedocs.io/en/stable/examples/bulk.html>
