Installation
============

This project uses Django 3.2, so requires Python >=3.6 and <3.11.

You can create a virtual environment as follows:

```
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Set up DB
=========

The following commands create the required database tables in a
local sqlite db, and load in some sample data.

```
source venv/bin/activate
cd ths
# run migrations
./manage.py migrate
# Load sample data
./manage.py loaddata sampledata.json
````

Run project
===========

```
source venv/bin/activate
cd ths
./manage.py runserver
````

This runs the Django devserver on port 8000.

You can now access the API using curl, e.g.

```
curl http://localhost:8000/listings/
```

or go to http://localhost:8000/listings/ in your browser


Run test suite
==============

```
source venv/bin/activate
cd ths
./manage.py test
````

Possible optimisations
==============

```
- pagination (implemented as example)
- Log and explain queries to see which tables could benefit from indexes
- put indexes on Assignment table: start_date and end_date?
- prefetch related records using select_related() as detailed here: https://www.velotio.com/engineering-blog/using-drf-for-faster-apis
- profile the performance as detailed here: https://www.dabapps.com/blog/api-performance-profiling-django-rest-framework/
````
