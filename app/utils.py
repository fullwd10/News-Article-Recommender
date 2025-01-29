from urllib.parse import urlparse, urljoin

# Split up URL into its separate components 
def parsed_url(url):
    return urlparse(url)

# Ensure urls are stored in the DB in a standard format i.e. no fragment section
def reduced_url(url):
    return parsed_url(url).scheme + '://' + parsed_url(url).netloc + parsed_url(url).path

# Convert relative URLs into absolute URLs
def join_url(base, url):
    return urljoin(base, url)

# URLs containing a fragment correspond to a comment section of a particular article - don't include these!
def url_fragment(url):
    return parsed_url(url).fragment

def is_valid(url):
    return bool(parsed_url(url).netloc) and bool(parsed_url(url).scheme)

