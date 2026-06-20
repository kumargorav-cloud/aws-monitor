# AWS Monitor

A collection of Python automation tools for AWS infrastructure monitoring and security auditing.

## Tools

### 1. Fleet Disk Monitor (aws-monitor-script.py)
Automatically discovers running EC2 instances and checks disk usage via SSH, sending Slack alerts for high usage.

### 2. Security Auditor (sg_boto3.py)
Checks AWS account for security risks:
- Security groups with sensitive ports open to the world (22, 3306, 5432)
- S3 buckets without public access protection
- Missing CloudTrail logging
Sends Slack alerts for each finding.

## Tech Stack
Python, boto3, paramiko, AWS (EC2, S3, CloudTrail), Slack Webhooks

## Setup
1. pip install boto3 paramiko requests
2. aws configure
3. export SLACK_WEBHOOK_URL="your-webhook-url"
4. Run: python3 aws-monitor-script.py OR python3 sg_boto3.py

## Skills Demonstrated
AWS automation, security auditing, SSH automation, Slack integration, secrets management
