import json

def lambda_handler(event, context):
    import boto3
    from datetime import datetime, timezone
    
    cw = boto3.client('cloudwatch')
    ec3 = boto3.client('ec2')
    hell = []
    dictlist = []
    regions = ec3.describe_regions().get('Regions',[] )
    for region in regions:
        reg=region['RegionName']
        ec2 = boto3.resource('ec2',region_name=reg)
        for instance in ec2.instances.all():
            insta = instance.id 
            t = datetime.now(timezone.utc)
            w = datetime.now(timezone.utc) - instance.launch_time
            dict = instance.state
            for value in dict.values():
                dictlist.append(value)
            if (dictlist[1] == "running"):
                if (w.total_seconds() > 36000):
                    print()
                    print()
                    print(reg)
                    print (insta)
                    print ("greater than 10 hours")
                    ec3.stop_instances(InstanceIds=[insta])
                else:
                    print()
                    print(reg)
                    print (insta)
                    
                    print ("less than 10 hours")
            else:
                print("no running instances")
    print()
    print()
    
