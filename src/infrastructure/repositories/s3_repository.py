import boto3
from botocore.exceptions import NoCredentialsError, ClientError

class S3Repository:
    _instance = None

    def __new__(cls, access_key, secret_key):
        if not cls._instance:
            cls._instance = super(S3Repository, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, access_key, secret_key):
        if self._initialized:
            return
        self._initialized = True
        self.access_key = access_key
        self.secret_key = secret_key

        self.s3 = boto3.client('s3', aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key)
        self.s3_resource = boto3.Session(aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key).resource('s3')

    def read_all_objects(self, bucket_name):
        """
        Reads all object keys in the specified S3 bucket.

        Parameters:
        - bucket_name (str): The name of the S3 bucket.

        Returns:
        - list: A list containing all object keys in the specified bucket.
        """
        try:
            keys=[]
            response = self.s3_resource.Bucket(bucket_name).objects.all()
            for obj in response:
                keys.append(obj.key)
            return keys
        except ClientError: 
            print("Invalid bucket name")
            return []
        except NoCredentialsError:
            print("Credentials not available or incorrect.")
            return []

    def remove_object(self, bucket_name, resourceKey):
        """
        Removes an object from the specified S3 bucket.

        Parameters:
        - bucket_name (str): The name of the S3 bucket.
        - resourceKey (str): The key of the object to be removed.

        Returns:
        - bool: True if the object was successfully removed, False otherwise.
        """
        try:
            self.s3.delete_object(Bucket=bucket_name, Key=resourceKey)
            print(f"Object '{resourceKey}' removed from S3 bucket '{bucket_name}'.")
            return True
        except NoCredentialsError:
            print("Credentials not available or incorrect.")
            return False

    def upload_object(self, bucket_name, local_path, resourceKey):
        """
        Uploads an object to the specified S3 bucket.

        Parameters:
        - bucket_name (str): The name of the S3 bucket.
        - local_path (str): The local path of the file to be uploaded.
        - resourceKey (str): The key under which to store the object in the S3 bucket.

        Returns:
        - bool: True if the object was successfully uploaded, False otherwise.
        """
        try:
            self.s3.upload_file(local_path, bucket_name, resourceKey)
            print(f"Object uploaded to S3 bucket '{bucket_name}' with key '{resourceKey}'.")
            return True
        except NoCredentialsError:
            print("Credentials not available or incorrect.")
            return False
        
    def download_object(self, bucket_name, local_path, resourceKey):
        """
        Download an object to the specified S3 bucket.

        Parameters:
        - bucket_name (str): The name of the S3 bucket.
        - local_path (str): The local path of the file to be uploaded.
        - resourceKey (str): The key under which to store the object in the S3 bucket.

        Returns:
        - bool: True if the object was successfully uploaded, False otherwise.
        """
        try:
            self.s3.download_file(bucket_name, resourceKey, local_path)
            print(f"Object downloaded from S3 bucket '{bucket_name}' with key '{resourceKey}'.")
            return True
        except NoCredentialsError:
            print("Credentials not available or incorrect.")
            return False