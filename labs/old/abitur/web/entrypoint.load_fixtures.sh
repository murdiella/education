echo "Activating virtual environment..." >&2

. /venv/bin/activate

echo "Waiting for database to start" >&2

sleep 45


for fixture in apps/*/fixtures/*.json
do
  python3 manage.py loaddata $fixture
done

while true
do
  sleep 1
done
