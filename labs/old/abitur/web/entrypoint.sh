echo "Activating virtual environment..." >&2

. /venv/bin/activate

echo "Migrating the database..." >&2

while ! python manage.py migrate
do
  echo "Waiting for db to start..." >&2
  sleep 1
done

echo "Collecting static files..." >&2

echo "yes" | python manage.py collectstatic

echo "Starting up an application server..." >&2

daphne -b 0.0.0.0 -p 8000 settings.asgi:application
