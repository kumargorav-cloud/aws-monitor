# AWS Monitor Script

A Python automation tool that automatically discovers all running 
AWS EC2 instances and checks their disk usage via SSH.

## What it does
- Uses boto3 to query AWS and find all running EC2 instances
- Automatically SSHes into each instance using paramiko
- Parses disk usage output and flags partitions above threshold
- Logs alerts with timestamps

## Tech Stack
- Python 3
- boto3 (AWS SDK)
- paramiko (SSH automation)
- AWS EC2

## How to run
1. Install dependencies:
   pip install boto3 paramiko

2. Configure AWS credentials:
   aws configure

3. Update key_path in aws-monitor-script.py with your .pem file path

4. Run:
   python aws-monitor-script.py

## Skills demonstrated
- AWS infrastructure automation
- Python scripting
- SSH automation
- Real-time monitoring