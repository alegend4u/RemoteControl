# WebTop
Remote control your desktop using a web application.

## Setup Instructions.

1. Clone the repo.
2. Create a virtual environment of your choice (conda, venv etc.) and install packages using requirements.txt: `pip install -r requirements.txt`
3. Migrate the database: `python manage.py migrate`
4. Create a superuser: `python manage.py createsuperuser` and enter desired credentials.
5. Run the server: `python manage.py runserver 0:8000` (Development server)
6. Use `localhost:8000/admin` to access admin panel and approve the clients' request to allow control.

Note: For development purposes, currently `db.sqlite3` is used. Feel free to chamge DB config in `WebTop/settings.py`
