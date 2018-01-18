import boto3

class S3_client:

    #Intializing object
    #bucket_names consists of strings that represnt names of created buckets at S3 service
    #bucket_loc specifies locations for bucket creation
    def __init__(self):
        self.bucket_names=[]
        self.client = boto3.client('s3') #creates a S3 client


    #Method for bucket creation using create_bucket() method
    #S3 client should be placed in the location where new bucket is created
    def createBuckets(self, bucket_name, bucket_loc):
        try:
            s3 = boto3.client('s3', bucket_loc)
            response = s3.create_bucket(ACL='public-read-write',
                             Bucket=bucket_name,
                             CreateBucketConfiguration={
                                 'LocationConstraint': bucket_loc
                             })
        except Exception as e:
            return e

        return "OK"

    def deleteBucket(self, bucket_name, bucket_loc):
        try:
            s3 = boto3.client('s3', bucket_loc)
            response = s3.delete_bucket(Bucket=bucket_name)
        except Exception as e:
            return e
        return "OK"


    #Shows successufuly created buckets using list_bucket() method
    def showBuckets(self):
        response = self.client.list_buckets()
        result=[]
        for bucket in response["Buckets"]:
            result.append(bucket)
        return result

    #Adds object to bucket
    #name - object name (name of file)
    #bucket - bucket name
    def addObject(self, name, bucket):
        try:
            data = open(name, 'rb')
            self.client.put_object(
                ACL= 'public-read-write',
                Body= data,
                Bucket=bucket,
                Key=name
                )
        except Exception as e:
            return e
        return "OK"

    #Deletes object from bucket
    #name - object name (name of file)
    #bucket - bucket name
    def deleteObject(self, name, bucket):
        try:
            data = open(name, 'rb')
            self.client.delete_object(Bucket=bucket, Key=name)
        except Exception as e:
            return e
        return "OK"

     # Downloads object from bucket
     # name - object name (name of file)
     # bucket - bucket name
    def downloadObject(self, name, bucket, saveAsname):
        try:
            self.client.download_file(bucket, name, saveAsname)
        except Exception as e:
            return e
        return "OK"






