import os
import sys
import argparse
import requests
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

def download_file(url, filename, progress_bar):
    try:
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024

        with open(filename, 'wb') as file:
            for data in response.iter_content(chunk_size=block_size):
                file.write(data)

        progress_bar.update(1)
    except Exception as e:
        print(f'Error downloading {filename}: {e}')

def dl(key, num_files, sign):
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        progress_bar = tqdm(total=num_files, desc='Overall Progress')

        for i in range(1, num_files + 1):
            n = f'{i:03}'
            file_url = f'https://d17h7bm6klmafz.cloudfront.net/{key}/hls/720/{n}.ts?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9kMWQzNHA4dno2M29pcS5jbG91ZGZyb250Lm5ldC8yZTNjYmI1NS02YWRjLTRkYzAtODA4Ny0yNDMxOGIyNDJmMGMvKiIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTcxMDQ3OTg1NX19fV19&Key-Pair-Id=APKAJBP3D6S2IU5JK4LQ&Signature={sign}'
            filename = f'{n}.ts'
            futures.append(executor.submit(download_file, file_url, filename, progress_bar))

        for future in futures:
            future.result()

        progress_bar.close()

def main():
    parser = argparse.ArgumentParser(description='Download files using multithreading.')
    parser.add_argument('key', help='KEY')
    parser.add_argument('num_files', type=int, help='Number of files to download')
    parser.add_argument('sign',help="Signature ID")

    args = parser.parse_args()
    KeyboardInterrupt = args.key
    dl(args.key, args.num_files, args.sign)

if __name__ == '__main__':
    main()