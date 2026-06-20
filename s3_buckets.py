import boto3

s3 = boto3.client('s3')
Buckets = s3.list_buckets()['Buckets']

for bucket in Buckets:
    name = bucket['Name']
    try:
        result = s3.get_public_access_block(Bucket=name)
        print(name,result['PublicAccessBlockConfiguration'])
    except Exception as e:
        print(name, "Error:",e)


