import os

def split_aws_key(key):
    """
    Splits the AWS key into UUID and extension.

    Parameters:
    - key (str): AWS key.

    Returns:
    - uuid (str): UUID of the key.
    - extension (str): Extension of the key.
    """
    try:
        filename, _ = os.path.splitext(key)
        uuid = filename.split('/')[-1]
        extension = os.path.splitext(key)[1]

        print(f"UUID: {uuid}, Extension: {extension}")
        
        return uuid, extension
    
    except Exception as e:
        print(f"Error splitting AWS key: {e}")