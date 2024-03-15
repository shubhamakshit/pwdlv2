import threading
import sys
import requests

# Define the number of threads you want to use
num_threads = 100  # For example, using 5 threads
DIFFERENCE = 20
worker_info = {}


def download_file(worker, init=0, final=0, key=None, sign=None):
    num = init
    if worker not in worker_info:
        worker_info[worker] = {}
        print(f'Worker {worker} has joined the dl')
    if num == 1:
        num = 0
    file = num
    if num < 10:
        file = f'00{num}'
    elif num < 100:
        file = f'0{num}'

    while num <= final:
        url = f'https://d17h7bm6klmafz.cloudfront.net/{key}/hls/720/{file}.ts?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9kMWQzNHA4dno2M29pcS5jbG91ZGZyb250Lm5ldC8yZTNjYmI1NS02YWRjLTRkYzAtODA4Ny0yNDMxOGIyNDJmMGMvKiIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTcxMDQ3OTg1NX19fV19&Key-Pair-Id=APKAJBP3D6S2IU5JK4LQ&Signature={sign}'
        response = requests.get(url)
        if response.status_code == 200:
            with open(f"{file}.ts", 'wb') as f:
                f.write(response.content)
            num += 1
            file = num
            if num < 10:
                file = f'00{num}'
            elif num < 100:
                file = f'0{num}'


# Extracting key and sign from command-line arguments
if len(sys.argv) != 3:
    print("Usage: python script.py <KEY> <SIGN>")
    sys.exit(1)

KEY = sys.argv[1]
SIGN = sys.argv[2]

# Create and start threads
threads = []
for x in range(num_threads):
    x = x + 1
    init = (x - 1) * DIFFERENCE + 1
    final = x * DIFFERENCE
    thread = threading.Thread(target=download_file, args=(x, init, final, KEY, SIGN))
    thread.start()
    threads.append(thread)

# Wait for all threads to complete
for thread in threads:
    thread.join()
