import re 

def is_email(string: str) -> bool:
    """
    Check whether the given string is an email
    """
    pattern = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    return re.match(pattern, string) is not None

def username(email: str) -> str:
    """
    Fetch the username from an email
    """
    pattern = r'^(\w+)@'
    _match = re.match(pattern,email)
    return _match.group(1) if _match else None 

def domainname(email: str) -> str:
    """
    Fetch the domain name from an email
    """
    pattern = r'@(\w+[\.\w+]*)'
    _match = re.search(pattern, email)
    return _match.group(1) if _match else None