import sys
from red import find_final_url
import os
from parsev3 import remove_query_params
from post import extract_last_segment_number, post_op

if os.path.exists('./main.m3u8'): os.system('rm -f ./main.m3u8') # remove already existing m3u8 file
if os.path.exists('./enc.key'):   os.system('rm -f ./enc.key')   # remove already existing key file

# Check if command line arguments are provided correctly
if len(sys.argv) < 3:
    print("Usage: python script.py <KEY> <NAME>")
    sys.exit(1)

# Extract the key and name from command line arguments
KEY = sys.argv[1]
NAME = sys.argv[2]

# Generate the final URL using the key
final_url = find_final_url(f'http://psitoffers.store/1dm.php?vid={KEY}')

# Print each part of the final URL on a separate line
print("Final URL:")
print('\n'.join(final_url.split('&')))

# Download using aria2c
os.system(f"aria2c '{final_url.replace('master.m3u8', 'hls/720/main.m3u8')}'")
if os.path.exists('main.m3u8'):
    try:
        with open('main.m3u8','r') as mfile:
            m3u8_content = mfile.read()
            # Extract URL and query parameters
            url, query = remove_query_params(final_url)

            # Run dl.py script with the key and signature
            print(f"{os.system('clear')} Command [ python3 dlv2.py {KEY} {extract_last_segment_number(m3u8_content)} {query['Signature'][0]} ]")
            os.system(f"python3 dlv2.py {KEY} {extract_last_segment_number(m3u8_content)} {query['Signature'][0]}")
            post_op()
    except Exception as e:
        print(f"Error occured: {e}")


os.system(f'ffmpeg -allowed_extensions ALL -y -i main.m3u8 -c copy {NAME}.mp4')

os.system('rm -rf *ts*')

