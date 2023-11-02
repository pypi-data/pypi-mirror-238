import os  
import boto3

def manage_rds_clusters(region, action):
    try:
        # Initialize AWS clients for RDS
        rds = boto3.client('rds', region_name=region)

        db_cluster_identifiers = os.getenv('db_cluster_identifiers')
        if db_cluster_identifiers is None:
            raise ValueError(f"Unknown db_cluster_identifiers: {db_cluster_identifiers}")

        db_clusters = [cluster.strip() for cluster in db_cluster_identifiers.split(',')]

        for cluster in db_clusters:
            response = rds.describe_db_clusters(DBClusterIdentifier=cluster)
            cluster_status = response['DBClusters'][0]['Status']
            print(f"Current Cluster {cluster} Status is: {cluster_status}")

            if action == "start" and cluster_status == "available":
                print(f"RDS Cluster {cluster} is already in available state. Skipping start action.")

            elif action == "stop" and cluster_status == "stopped":
                print(f"RDS Cluster {cluster} is already in stopped state. Skipping stop action.")

            elif action == "start" and cluster_status != "available":
                print(f"Starting RDS Cluster {cluster}...")
                rds.start_db_cluster(DBClusterIdentifier=cluster)

            elif action == "stop" and cluster_status != "stopped":
                print(f"Stopping RDS Cluster {cluster}...")
                rds.stop_db_cluster(DBClusterIdentifier=cluster)
    except Exception as err:
        print(f"There has been an error while performing Action: {action} on rds clusters ==> {err}")
