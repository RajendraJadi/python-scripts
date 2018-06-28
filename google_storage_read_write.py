from google.cloud import storage
import sys, os
from oauth2client.client import GoogleCredentials
credentials = GoogleCredentials.get_application_default()



# bucket = '/gs/my-bucket'

def writeText(bucketPath, contents):
    """
    https://cloud.google.com/storage/docs/object-basics#storage-download-object-python
    """
    client = storage.Client()
    bucket = client.get_bucket("solr-backups-dev-1")
    # Create a new blob and upload the file's content.
    blob = bucket.blob(bucketPath)
    blob.upload_from_string(contents)



def list_blobs(bucketPath):
    print("storage client")
    client = storage.Client()
    print("gettig bucket")
    bucket = client.get_bucket('solr-backups-dev-1')
    # Create a new blob and upload the file's content.
    blobs = bucket.list_blobs()
    for blob in blobs:
        print(blob.name)


def write(bucketPath):
    client = storage.Client()
    print("gettig bucket")
    bucket = client.get_bucket("solr-backups-dev-1")
    print("got bucket")
    blob = bucket.blob("test.gz")
    print("blob")
    # with open('backup', 'rb') as my_file:
    blob.upload_from_filename(filename='backup.gz')
    print("upload")




if __name__ == '__main__':
    #write("solr-backups-dev-1")
    list_blobs("solr-backups-dev-1")
    #readText("solr-backups-dev-1")
    # list_blobs("log-analysis-output-dev-1")

