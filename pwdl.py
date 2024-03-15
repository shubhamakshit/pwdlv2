import sys
from red import find_final_url
import os
from parsev3 import remove_query_params

if os.path.exists('./main.m3u8'): os.system('rm -f ./main.m3u8') # remove already existing m3u8 file
if os.path.exists('./enc.key'):   os.system('rm -f ./enc.key')   # remove already existing key file

# Check if command line arguments are provided correctly
if len(sys.argv) < 2:
    print("Usage: python script.py <KEY>")
    sys.exit(1)

# Extract the key from command line arguments
KEY = sys.argv[1]

# Generate the final URL using the key
final_url = find_final_url(f'http://psitoffers.store/1dm.php?vid={KEY}')

# Print each part of the final URL on a separate line
print("Final URL:")
print('\n'.join(final_url.split('&')))

# Download using aria2c
os.system(f"aria2c '{final_url.replace('master.m3u8', 'hls/720/main.m3u8')}'")
os.system('python3 post.py')

#Extract URL and query parameters
url, query = remove_query_params(final_url)

# Run dl.py script with the key and signature
os.system(f"python3 dl.py {KEY} {query['Signature'][0]}")

os.system(f'ffmpeg -allowed_extensions ALL -y -i main.m3u8 -c copy {KEY}.mp4')

os.system('rm -rf *ts*')

