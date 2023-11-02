import os  
import boto3
import yaml   # parsing yaml file for default config values

def manage_ecs_clusters(region, action):
    try:
        # Initialize AWS clients for ECS
        ecs = boto3.client('ecs', region_name=region)

        # Load the YAML file
        with open('default_config.yaml', 'r') as yaml_file:
            config = yaml.safe_load(yaml_file)

        start_desired_count = int(os.getenv('start_desired_count')) if os.getenv('start_desired_count') else 1
        stop_desired_count  = int(os.getenv('stop_desired_count'))  if os.getenv('stop_desired_count')  else 0

        all_cluster_name = os.getenv('cluster_name')
        if all_cluster_name :
            cluster_list = [cluster.strip() for cluster in all_cluster_name.split(',')]

        else:
            print(f"no cluster name was provided. Applying Action: {action} on all the ecs clusters")
            ecs_clusters = ecs.list_clusters()
            cluster_list = ecs_clusters['clusterArns']

        for cluster in cluster_list:
            ecs_cluster_response = ecs.describe_clusters(clusters=[cluster])

            if(ecs_cluster_response['clusters'][0] is None):
                print(f"ecs_cluster_response['clusters'][0] is None")
                return

            if ecs_cluster_response['clusters'][0]['status'] == 'INACTIVE':
                print(f'ECS Cluster {cluster} is in INACTIVE state. It must be ACTIVE')
                return

            ecs_service_response = ecs.list_services(cluster=cluster)
            services = ecs_service_response['serviceArns']
            for service in services:
                service_response = ecs.describe_services(
                    cluster=cluster,
                    services=[service]
                )
                service_details = service_response['services'][0]
                desired_count = service_details['desiredCount']

                if action == 'start' and desired_count > 0:
                    print(f'ECS Cluster {cluster} is already running.')

                elif action == 'stop' and desired_count == 0:
                    print(f'ECS Cluster {cluster} is already stopped.')

                elif action == 'start' and desired_count == 0:
                    for service in services:
                        ecs.update_service(
                            cluster=cluster,
                            service=service,
                            desiredCount=start_desired_count  # Set the desired task count to the desired value
                        )
                        print(f'Starting service: {service}')

                    print(f'All services in cluster {cluster} have been started.')

                elif action == 'stop' and desired_count > 0:
                    for service in services:
                        ecs.update_service(
                            cluster=cluster,
                            service=service,
                            desiredCount=stop_desired_count
                        )
                        print(f'Stopping service: {service}')

                    print(f'All services in cluster {cluster} have been stopped.')
    except Exception as err:
        print(f"There has been an error while performing Action: {action} on ecs clusters ==> {err}")
