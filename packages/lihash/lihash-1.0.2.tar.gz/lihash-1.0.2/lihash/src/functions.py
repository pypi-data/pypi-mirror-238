import hashlib

def hash_string(string_object:str, n:int=12) -> int:
    """It hashes a string object to fix length integer

    Args:
        string_object (str): string object
        n (int, optional): the length of output. Defaults to 12.

    Returns:
        int: hash value of max length n digits
    """
    int__ = int(hashlib.sha1(string_object.encode("utf-8")).hexdigest(), 18) % (10**n)
    int_s = str(int__)
    if len(int_s) < n:
        int_s = int_s + "0"*(n-len(int_s))
    if len(int_s) > n:
        int_s = int_s[:n]
    return int(int_s)