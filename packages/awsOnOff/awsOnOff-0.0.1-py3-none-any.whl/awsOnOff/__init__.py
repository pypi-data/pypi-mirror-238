import awsOnOff.ec2 as ec2

def start_ec2(instance_id , region):
    if not region:
        raise Exception("Must Provide Region")
    if not instance_id:
        raise Exception("Must Provide instance_id")

    if(type(instance_id).__name__ == 'str'):
        instance_id_list = [ids.strip() for ids in instance_id.split(',')]
    
    ec2.manage_ec2_instance(instance_id_list , region , 'start')

def start_all_ec2(region):
    if not region:
        raise Exception("Must Provide Region")

    ec2.manage_ec2_instance( 'all' , region , 'start')

def stop_ec2(instance_id , region):
    if not region:
        raise Exception("Must Provide Region")
    if not instance_id:
        raise Exception("Must Provide instance_id")

    if(type(instance_id).__name__ == 'str'):
        instance_id = [ids.strip() for ids in instance_id.split(',')]
    
    ec2.manage_ec2_instance(instance_id , region , 'stop')

def stop_all_ec2(region):
    if not region:
        raise Exception("Must Provide Region")

    ec2.manage_ec2_instance( 'all' , region , 'stop')
