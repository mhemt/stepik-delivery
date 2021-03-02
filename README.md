# How to run

Create and activate virtual environment:
```
python3 -m venv venv
source venv/bin/activate
```

Install all dependencies:
```
pip install -r requirements.txt
```

Migrate to DB:
```
python manage.py migrate
```

Import data (already done):
```
python manage.py import_items
python manage.py import_reviews
python manage.py import_users
```

Run Django server:
```
python manage.py runserver
```

Open link in browser, e.g.:
```
http://127.0.0.1:8000/api/v1/items/1/
```
