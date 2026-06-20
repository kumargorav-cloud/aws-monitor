import boto3
import os
import requests

#getting the slack api
webhook_url = os.environ.get("SLACK_WEBHOOK_URL")

#writing a function to send the msg to slack
def send_slack_alert(message):
    requests.post(webhook_url, json={"text": message})

#function to check security groups
def check_security_groups():
        try:
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
            return True
        except Exception as e:
            print(f"Security group check failed: {e}")
            return False
        

#function to check s3 buckets
def check_s3_bucket():
    try:
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
                msg = f"WARNING: could not check public access for bucket [{name}] - Error: {e}"
                print(msg)
                send_slack_alert(msg)
        return True
    except Exception as e:
        print(f"failed to access the bucket list, Error: {e}")
        return False



#function to check cloudtrail
def check_cloudtrail():
    try:
        ct = boto3.client('cloudtrail',region_name = "ap-south-1")
        response = ct.describe_trails()
        if len(response['trailList']) == 0:
            msg = "WARNING: No CloudTrail trails configured - account activity is NOT being logged"
            print(msg)
            send_slack_alert(msg)
        return True
    except Exception as e:
        print(f"Failed to check cloudtrail,Error: {e} ")
        return False


results = {
    "Security_groups":check_security_groups(),
    "S3 buckets": check_s3_bucket(),
    "check cloud trail":check_cloudtrail()
}

passed = 0
failed = 0

for check_name, result in results.items():
    if result:
        passed+=1
    else:
        failed+=1
        print(f"{check_name} check did not complete successfully")

print(f"\nSummary: {passed} checks completed, {failed} checks failed")

