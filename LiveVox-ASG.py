import boto3
import subprocess
from datetime import date

session = boto3.Session(profile_name="default")
ec2_inst = session.client(service_name='ec2')

# Creating Launch Template
launch_tp = ec2_inst.create_launch_template(
    LaunchTemplateName = "LiveVox-Launch-Template",
    LaunchTemplateData={
        'ImageId': 'ami-06e46074ae430fba6',
        'InstanceType' : "t2.micro",
        'KeyName' : "terraform-key",
        'Monitoring': {
            'Enabled': True
        }                                
    }
)
template_id = launch_tp['LaunchTemplate']['LaunchTemplateId']

# Creating ASG from above Launch template
asg = session.client('autoscaling').create_auto_scaling_group(
    AutoScalingGroupName = "LiveVox-ASG",
    LaunchTemplate={
        'LaunchTemplateId': template_id,
    },
    MinSize=3,
    MaxSize=6,
    DesiredCapacity=3,
    AvailabilityZones=[
        "us-east-1a",
        "us-east-1b",
        "us-east-1c"
    ]
)

# Finding uptime of EC2 instances
subprocess.run('aws ec2 describe-instances --query Reservations[].Instances[].[LaunchTime]')

# Describing Scheduled actions
response = session.client('autoscaling').describe_scheduled_actions(
    AutoScalingGroupName = "LiveVox-ASG"
)
print(response)