import boto3
import paramiko
import requests

webhook_url = "your-slack-webhook-url-here"

def send_slack_alert(message):
    requests.post(webhook_url, json={"text": message})

# boto3 part — same as before
ec2 = boto3.client('ec2', region_name='ap-south-1')
response = ec2.describe_instances()

running_instances_ips = []
for reservation in response["Reservations"]:
    for instance in reservation["Instances"]:
        state = instance['State']['Name']
        public_ip = instance.get('PublicIpAddress', None)
        if state == 'running' and public_ip:
            running_instances_ips.append(public_ip)

# paramiko part — same as before
for ip in running_instances_ips:
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username="ubuntu", key_filename="your-key-to-ssh-into-aws")
        stdin, stdout, stderr = client.exec_command("df -h")
        output = stdout.read().decode()
        lines = output.splitlines()[1:]
        for line in lines:
            value = int(line.split()[4].strip("%"))
            mount_point = line.split()[5]
            if value > 30:
                msg = f"WARNING: [{ip}] {mount_point} is at {value}% usage"
                print(msg)
                send_slack_alert(msg)
    finally:
        client.close()