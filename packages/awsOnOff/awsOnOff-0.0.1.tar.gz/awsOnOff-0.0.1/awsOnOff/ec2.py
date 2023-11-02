import boto3

def manage_ec2_instance(instance_id_list, region, action):
    try:
        # Initialize AWS clients for EC2
        ec2 = boto3.client('ec2', region_name=region)
        all_instance_id = instance_id_list

        if( type(instance_id_list).__name__ == 'str' and instance_id_list == 'all' ):
            instance_id_list = [instance['InstanceId'] for reservation in ec2.describe_instances()['Reservations'] for instance in reservation['Instances']]
        
        for instance_id in instance_id_list:
            print(f"Applying Action: {action} on ec2 instance with instance_id: {instance_id}")
    
            state = get_instance_state(instance_id , ec2)
    
            if state == 'running' and action == 'start':
                print(f'Instance {instance_id} is already running.')
            elif state == 'stopped' and action == 'stop':
                print(f'Instance {instance_id} is already stopped.')
            elif state in ['pending', 'stopping', 'stopped', 'terminating'] and action == 'start':
                print(f'Starting instance {instance_id}...')
                ec2.start_instances(InstanceIds=[instance_id])
            elif state == 'running' and action == 'stop':
                print(f'Stopping instance {instance_id}...')
                ec2.stop_instances(InstanceIds=[instance_id])
            else:
                print(f'Instance {instance_id} is in an unsupported state for the requested action.')
                
    except Exception as err:
        print(f"There has been an error while performing Action: {action} on ec2 instances ==> {err}")

def get_instance_state(instance_id , ec2) :
    response = ec2.describe_instances(InstanceIds=[instance_id])
    state = response['Reservations'][0]['Instances'][0]['State']['Name']
    return state
