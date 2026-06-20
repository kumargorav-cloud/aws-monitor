import boto3
import os
import requests

webhook_url = os.environ.get("SLACK_WEBHOOK_URL")

def send_slack_alert(message):
    requests.post(webhook_url, json={"text": message})

def check_security_groups():
    ec2 = boto3.client('ec2',region_name = "ap-south-1")
    response = ec2.describe_security_groups()

    for element in response['SecurityGroups']:
        for protocols in element['IpPermissions']:
            port = protocols.get('FromPort')
            if port in [22,3306,5432]:
                for ranges in protocols['IpRanges']:
                    if ranges['CidrIp'] == "0.0.0.0/0":
                        msg = (f"WARNING: [{element['GroupName']}] Port {protocols['FromPort']} open to the world (0.0.0.0/0)")
                        print(msg)
                        send_slack_alert(msg)

def check_s3_bucket():
    s3 = boto3.client('s3')
    Buckets = s3.list_buckets()['Buckets']

    for bucket in Buckets:
        name = bucket['Name']
        try:
            result = s3.get_public_access_block(Bucket=name)
            configs = result['PublicAccessBlockConfiguration']

            if not configs['BlockPublicAcls'] or not configs['IgnorePublicAcls'] or not configs['BlockPublicPolicy'] or not configs['RestrictPublicBuckets']:
                msg = f"WARNING: s3 bucket [{name}] is not fully protected from public access"
                print(msg)
                send_slack_alert(msg)

        except Exception as e:
            msg = f"WARNING: s3 bucket [{name}] has NO public access block configuration"
            print(msg)
            send_slack_alert(msg)


def check_cloudtrail():
    ct = boto3.client('cloudtrail',region_name = "ap-south-1")
    response = ct.describe_trails()
    if len(response['trailList']) == 0:
        msg = "WARNING: No CloudTrail trails configured - account activity si NOT being logged"
        print(msg)
        send_slack_alert(msg)
    else:
        print("CloudTrail is configured")
    



check_security_groups()
check_s3_bucket()
check_cloudtrail()
