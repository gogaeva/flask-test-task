#!/bin/bash

flask run --host 0.0.0.0 --port 8080 &
sleep 10
pid=$(pgrep -f "flask run")
python3 memory_checker.py $pid
