from urllib.parse import urlparse, parse_qs, urlunparse

def remove_query_params(url):
    # Parse the URL
    parsed_url = urlparse(url)
    
    # Extract query parameters
    query_params = parse_qs(parsed_url.query)
    
    # Remove the query parameters
    parsed_url = parsed_url._replace(query=None)
    
    # Reconstruct the URL without the query parameters
    url_without_params = urlunparse(parsed_url)
    
    return url_without_params, query_params
