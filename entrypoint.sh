alembic upgrade head

if [ "$TARGET" == "test" ]; then
  python -m unittest
else
  while true; do
    python3 main.py
  done
fi
