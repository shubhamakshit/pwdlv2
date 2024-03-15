import sys
import requests

def find_final_url(initial_url):
    try:
        response = requests.head(initial_url, allow_redirects=True)
        final_url = response.url
        return final_url
    except requests.RequestException as e:
        print("An error occurred:", e)
        return None

# if __name__ == "__main__":
#     if len(sys.argv) != 2:
#         print("Usage: python script.py <key>")
#         sys.exit(1)

#     key = sys.argv[1]
#     initial_url = f"http://psitoffers.store/1dm.php?vid={key}"
#     final_url = find_final_url(initial_url)

#     if final_url:
#         print("Final URL:", final_url)
#     else:
#         print("Unable to find the final URL.")

