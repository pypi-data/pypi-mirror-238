from urllib.parse import urlparse

def isURL(input_string : str) -> bool:
    try:
        # Try parsing the string as a URL
        result = urlparse(input_string)
        if all([result.scheme, result.netloc]):
            return True
    except Exception as e:
        pass  # If an exception occurs, it's likely not a URL
    
    return False