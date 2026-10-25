#bin/bash

python3 signal-filter.py
echo "filtered data and aquired relevant data"

echo "training model..."
python3 main.py
