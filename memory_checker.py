import argparse
import psutil
import requests
import time

HOST = 'http://localhost:8080' 

parser = argparse.ArgumentParser()
parser.add_argument('pid', type=int, help='PID of the process to check')
args = parser.parse_args()
pid = args.pid

process = psutil.Process(pid)

res = requests.get(f'{HOST}/limits?category=memory')
limit_in_megabytes = int(res.json()['value'])
limit = limit_in_megabytes * 1024 * 1024

while True:
    mem_info = process.memory_info().rss
    if mem_info > limit:
        print(f'Memory usage exceeded limit: {mem_info} > {limit}')
        requests.get(f'{HOST}/alarm')
    time.sleep(1)


