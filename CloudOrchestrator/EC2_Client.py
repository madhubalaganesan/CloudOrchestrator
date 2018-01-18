import json

import boto3
from datetime import datetime, timedelta

class EC2_client():
    def __init__(self):
        self.AMIs={"us-east-2" : "ami-15e9c770", "us-east-1": "ami-55ef662f",
                      "us-west-1": "ami-a51f27c5", "us-west-2": "ami-bf4193c7",
                      "ap-south-1": "ami-d5c18eba", "ap-northeast-2": "ami-1196317f",
                      "eu-central-1": "ami-bf2ba8d0", "eu-west-1": "ami-1a962263",
                      "eu-west-2": "ami-e7d6c983"}


    def showInstances(self, region):
        try:
            client = boto3.client('ec2', region_name=region)
            response = client.describe_instances()
        except Exception as e:
            return e
        return response


    def createInstance(self, name, region, type="t2.micro"):
        try:
            resource = boto3.resource('ec2', region_name=region)
            key_name=name+".pem"
            outfile = open(key_name, 'w')
            key_pair = resource.create_key_pair(KeyName=key_name)
            KeyPairOut = str(key_pair.key_material)
            outfile.write(KeyPairOut)
            instances = resource.create_instances(
            ImageId= self.AMIs[region],
            MinCount=1,
            MaxCount=1,
            KeyName="TestKey",
            InstanceType=type,
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': name
                        },
                    ]
                },
            ]
        )
        except Exception as e:
            return e
        return "OK"


    def getStatus(self, region, id):
        try:
            client = boto3.client('ec2', region_name=region)
            response = client.describe_instance_status(InstanceIds=[id])
        except Exception as e:
            return e
        return response

    def stopInstance(self, region, id):
        try:
            client = boto3.client('ec2', region_name=region)
            response = client.stop_instances(InstanceIds=[id])
        except Exception as e:
            return e
        return "OK"

    def startInstance(self, region, id):
        try:
            client=boto3.client('ec2', region_name=region)
            response = client.start_instances(InstanceIds=[id])
        except Exception as e:
            return e
        return "OK"

    def getMetricStat(self, id, metric='all', statistic='Average', period_min=5):
        watch = boto3.client('cloudwatch')
        if (metric=='all'):
            pass
        else:
            pass

    def plotMetricStat(self):
        pass




ec2 = EC2_client()
#ec2.showRegions()
#id = ec2.createInstance(False)
#print (id)
#id = 'i-087cb947db2ce4bbc'
#ec2.getStatus(id)
#ec2.stopInstance(id)

# response = ec2.showInstances('us-west-3')
# instances={}
# if 'Reservations' in response:
#     for elem in response['Reservations']:
#         if (elem):
#             if 'Tags' in elem['Instances'][0]:
#                 for tag in elem['Instances'][0]['Tags']:
#                     if tag['Key']=='Name':
#                         instances[tag['Value']]=elem['Instances'][0]['InstanceId']
#             else:
#                 instances['NONAME']=elem['Instances'][0]['InstanceId']
# print (instances)

