import subprocess
import boto3
import logging
import psycopg
from psycopg import OperationalError
import time
import argparse
import sys
from os import getenv
from botocore.exceptions import ClientError
import signal
from typing import Tuple, Union
from datetime import datetime, timedelta
import math


# Define type aliases
DBDetails = Tuple[str, str, str, str, str]  # (host, db, user, password, port)

ec2_client = boto3.client("ec2")
rds = boto3.client("rds")
cloudwatch = boto3.client("cloudwatch")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Script to configure RDS database storage size."
    )
    parser.add_argument("db_link", nargs="?", help="Name of the RDS database")
    return parser.parse_args()


def log_setup() -> None:
    logger = logging.getLogger()

    for handler in logger.handlers:
        logger.removeHandler(handler)
    handler = logging.StreamHandler(sys.stdout)

    dformat = "[%(filename)s:%(lineno)d] :%(levelname)8s: %(message)s"
    handler.setFormatter(logging.Formatter(dformat))
    logger.addHandler(handler)
    log_level = logging.INFO
    if getenv("DEBUG", False):
        log_level = logging.DEBUG
    logger.setLevel(log_level)

    # Suppress the more verbose modules
    logging.getLogger("botocore").setLevel(logging.WARN)
    logging.getLogger("s3transfer").setLevel(logging.WARN)
    logging.getLogger("boto3").setLevel(logging.WARN)
    logging.getLogger("urllib3").setLevel(logging.WARN)


def source_rds_instance(dbinstance: str) -> dict:
    return rds.describe_db_instances(DBInstanceIdentifier=dbinstance)["DBInstances"][0]

def get_db_details(db_link: str) -> DBDetails:
    # db_link = "postgres://{postgre_user}:{password}@{db_host}:{db_port}/{db_name}"

    user = db_link.split(":")[1].split("/")[-1]
    password = db_link.split(":")[2].split("@")[0]
    db = db_link.split("/")[-1]
    host = db_link.split(":")[2].split("@")[-1].split(".")[0]
    port = db_link.split(":")[3].split("/")[0]
    return host, db, user, password, port


def duplicate_rds(db_link: str, new_allocated_storage: int) -> dict:
    dbinstance , db, user, password, port = get_db_details(db_link)
    source_rds_data = source_rds_instance(dbinstance)

    instance_params = {
        "DBName": db,
        "DBInstanceIdentifier": f"{source_rds_data['DBInstanceIdentifier']}new",
        "AllocatedStorage": new_allocated_storage,
        "DBInstanceClass": source_rds_data["DBInstanceClass"],
        "Engine": source_rds_data["Engine"],
        "MasterUsername": user,
        "MasterUserPassword": password,
        "Port": int(port),
        "DBSecurityGroups": [
            items["DBSecurityGroupName"]
            for items in source_rds_data["DBSecurityGroups"]
        ],
        "VpcSecurityGroupIds": [
            items["VpcSecurityGroupId"]
            for items in source_rds_data["VpcSecurityGroups"]
        ],
        "AvailabilityZone": source_rds_data["AvailabilityZone"],
        "DBSubnetGroupName": source_rds_data["DBSubnetGroup"]["DBSubnetGroupName"],
        "PreferredMaintenanceWindow": source_rds_data["PreferredMaintenanceWindow"],
        "DBParameterGroupName": source_rds_data["DBParameterGroups"][0][
            "DBParameterGroupName"
        ],
        "BackupRetentionPeriod": source_rds_data["BackupRetentionPeriod"],
        "PreferredBackupWindow": source_rds_data["PreferredBackupWindow"],
        "MultiAZ": source_rds_data["MultiAZ"],
        "EngineVersion": source_rds_data["EngineVersion"],
        "AutoMinorVersionUpgrade": source_rds_data["AutoMinorVersionUpgrade"],
        "LicenseModel": source_rds_data["LicenseModel"],
        "OptionGroupName": source_rds_data["OptionGroupMemberships"][0][
            "OptionGroupName"
        ],
        "PubliclyAccessible": source_rds_data["PubliclyAccessible"],
        "Tags": source_rds_data["TagList"],
        "StorageType": (
            "gp3"
            if source_rds_data["StorageType"] == "gp2"
            else source_rds_data["StorageType"]
        ),
        "StorageEncrypted": source_rds_data["StorageEncrypted"],
        "KmsKeyId": source_rds_data["KmsKeyId"],
        "CopyTagsToSnapshot": source_rds_data["CopyTagsToSnapshot"],
        "EnableIAMDatabaseAuthentication": source_rds_data[
            "IAMDatabaseAuthenticationEnabled"
        ],
        "EnablePerformanceInsights": source_rds_data["PerformanceInsightsEnabled"],
        "DeletionProtection": source_rds_data["DeletionProtection"],
        "EnableCustomerOwnedIp": source_rds_data["CustomerOwnedIpEnabled"],
        "BackupTarget": source_rds_data["BackupTarget"],
        "NetworkType": source_rds_data["NetworkType"],
        "CACertificateIdentifier": source_rds_data["CACertificateIdentifier"],
    }

    try:
        if source_rds_data["MaxAllocatedStorage"]:
            instance_params["MaxAllocatedStorage"] = source_rds_data[
                "MaxAllocatedStorage"
            ]
    except KeyError:
        pass

    response = rds.create_db_instance(**instance_params)
    return response


def sync_dbs(old_db: str, new_db: str) -> bytes:
    # Create pgsync configuration with source and destination db details
    logging.info("Creating .pgsync.yml with source and destination db links")
    with open(".pgsync.yml", "w") as f:
        f.write(f"from: {old_db}\n")
        f.write(f"to: {new_db}\n")
        f.write("to_safe: true\n")
    # pgsync
    logging.info("Syncing DB's")
    try:
        process = subprocess.Popen(
            ["pgsync", "--schema-first", "--all-schemas"],
            stdout=subprocess.PIPE,
        )
        output = process.communicate()[0]
        if int(process.returncode) != 0:
            logging.error(f"Command failed. Return code : {process.returncode}")
        else:
            logging.info("Sync completed ")
        return output
    except Exception as e:
        logging.error(f"Issue with db sync -> {e}")
        exit(1)


def timeout_handler(signum: int, frame) -> None:
    raise TimeoutError("Timed out after as RDS is not ready to take connection")


def check_rds_availability(
    host: str, port: str, dbname: str, user: str, password: str
) -> Union[bool, None]:
    # Set a timeout for the function
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(600)  # 10 minutes in seconds

    while True:
        try:
            # Attempt to establish a connection to the RDS database
            conn = psycopg.connect(
                host=host, port=port, dbname=dbname, user=user, password=password
            )
            conn.close()
            logging.info(f"Connection established successfully with {host}.")
            time.sleep(90)
            return True

        except OperationalError:
            # If an OperationalError occurs (e.g., connection error), print the error
            logging.error(
                f"Error connecting to the RDS database {host}: Not ready to take connection yet."
            )
            logging.info("Retrying in 90 seconds...")
            time.sleep(90)

        except TimeoutError as e:
            logging.error(e)
            return False  # Indicate failure due to timeout

        finally:
            # Reset the alarm
            signal.alarm(0)


def rename_rds(old: str, new: str) -> dict:
    try:
        rds.modify_db_instance(
            DBInstanceIdentifier=old, NewDBInstanceIdentifier=new, ApplyImmediately=True
        )
        logging.info(f"DB renamed - {new}")
    except Exception as e:
        logging.error(f"Issue with renaming {old} -> {new} : {e}")
        exit(1)


def swap_db(old: str, new: str) -> None:
    logging.info(f"Renaming db: {old} -> {old}-old ")
    rename_rds(old, f"{old}-old")
    time.sleep(300)  # Adding time delay to wait for db renaming
    logging.info(f"Renaming db: {new} - > {old}")
    rename_rds(new, old)


def stop_rds(dbinstance: str) -> None:
    try:
        logging.info(f"Stopping the RDS instance - {dbinstance}")
        rds.stop_db_instance(DBInstanceIdentifier=dbinstance)
    except Exception as e:
        logging.error(f"Issue with stopping - {dbinstance} -> {e}")
        exit(1)


def allow_sgs(from_sg: str, to_sg: str, port: int) -> None:
    try:
        ec2_client.authorize_security_group_egress(
            GroupId=from_sg,
            IpPermissions=[
                {
                    "IpProtocol": "tcp",
                    "FromPort": port,
                    "ToPort": port,
                    "UserIdGroupPairs": [
                        {
                            "Description": "Lambda access",
                            "GroupId": to_sg,
                        }
                    ],
                }
            ],
        )
        logging.debug("Lambda outbound rule for sg '%s' done", from_sg)
    except ClientError as error:
        if error.response["Error"]["Code"] != "InvalidPermission.Duplicate":
            logging.error("sg egress change failed: %s", error)
            raise error
    try:
        ec2_client.authorize_security_group_ingress(
            GroupId=to_sg,
            IpPermissions=[
                {
                    "IpProtocol": "tcp",
                    "FromPort": port,
                    "ToPort": port,
                    "UserIdGroupPairs": [
                        {
                            "Description": "Lambda access",
                            "GroupId": from_sg,
                        }
                    ],
                }
            ],
        )
        logging.debug("inbound rule for sg '%s' done", to_sg)
    except ClientError as error:
        if error.response["Error"]["Code"] != "InvalidPermission.Duplicate":
            logging.error("sg ingress change failed: %s", error)
            raise error

    logging.info("ECS inbound rule SG '%s' -> '%s' done", from_sg, to_sg)


def revoke_sgs(from_sg: str, to_sg: str, port: int) -> None:
    try:
        ec2_client.revoke_security_group_egress(
            GroupId=from_sg,
            IpPermissions=[
                {
                    "IpProtocol": "tcp",
                    "FromPort": port,
                    "ToPort": port,
                    "UserIdGroupPairs": [
                        {
                            "Description": "Lambda access",
                            "GroupId": to_sg,
                        }
                    ],
                }
            ],
        )
        logging.debug("ECS outbound rule for sg '%s' removed", from_sg)
    except ClientError as error:
        if error.response["Error"]["Code"] != "InvalidPermission.NotFound":
            logging.error("sg egress change failed: %s", error)
            raise error
    try:
        ec2_client.revoke_security_group_ingress(
            GroupId=to_sg,
            IpPermissions=[
                {
                    "IpProtocol": "tcp",
                    "FromPort": port,
                    "ToPort": port,
                    "UserIdGroupPairs": [
                        {
                            "Description": "Lambda access",
                            "GroupId": from_sg,
                        }
                    ],
                }
            ],
        )
        logging.debug("inbound rule for sg '%s' removed", to_sg)
    except ClientError as error:
        if error.response["Error"]["Code"] != "InvalidPermission.NotFound":
            logging.error("sg ingress change failed: %s", error)
            raise error

    logging.info("SG '%s' -/-> '%s' done", from_sg, to_sg)


# rds monitoring data for free storage
def get_db_freestorage(DBInstanceIdentifier):
    response = cloudwatch.get_metric_data(
        MetricDataQueries=[
            {
                "Id": "fetching_FreeStorageSpace",
                "MetricStat": {
                    "Metric": {
                        "Namespace": "AWS/RDS",
                        "MetricName": "FreeStorageSpace",
                        "Dimensions": [
                            {
                                "Name": "DBInstanceIdentifier",
                                "Value": DBInstanceIdentifier,
                            }
                        ],
                    },
                    "Period": 86400 * 7,
                    "Stat": "Minimum",
                },
            }
        ],
        StartTime=(datetime.now() - timedelta(seconds=86400 * 7)).timestamp(),
        EndTime=datetime.now().timestamp(),
        ScanBy="TimestampDescending",
    )
    return round(response["MetricDataResults"][0]["Values"][0] / 1024**3, 2)


def evaluate_db_storage(dbinstance):
    free_storage = get_db_freestorage(dbinstance)
    allocated_storage = source_rds_instance(dbinstance)["AllocatedStorage"]
    used_storage = allocated_storage - free_storage
    new_allocated_storage = 1.2 * used_storage
    # gp3 min limit is 20 GB
    if new_allocated_storage < 20:
        return 20
    return math.ceil(new_allocated_storage)


def migrate_rds(db_link: str) -> None:
    dbinstance, db, user, password, port = get_db_details(db_link)
    size = evaluate_db_storage(dbinstance)
    source_rds_data = source_rds_instance(dbinstance)
    from_sg = getenv("SG_ID")
    to_sg = [
        items["VpcSecurityGroupId"] for items in source_rds_data["VpcSecurityGroups"]
    ][0]

    allow_sgs(from_sg, to_sg, int(port))
    logging.info(f" Creating the duplicte rds of {dbinstance}")

    logging.info(
        f"Duplicating the RDS instance {dbinstance} with {size} GB storage. \
        Existing storage -> {source_rds_instance(dbinstance)['AllocatedStorage']}"
    )
    new_rds_DBInstanceIdentifier = duplicate_rds(db_link, size)["DBInstance"][
        "DBInstanceIdentifier"
    ]

    logging.info(f"Creating {new_rds_DBInstanceIdentifier}")
    old_db_endpoint = source_rds_data["Endpoint"]["Address"]
    new_db_endpoint = (
        new_rds_DBInstanceIdentifier + "." + ".".join(old_db_endpoint.split(".")[1:])
    )
    check_rds_availability(new_db_endpoint, port, db, user, password)

    # DB sync
    source_db_link = f"postgresql://{user}:{password}@{old_db_endpoint}:{port}/{db}"
    destination_db_link = (
        f"postgresql://{user}:{password}@{new_db_endpoint}:{port}/{db}"
    )
    sync_dbs(source_db_link, destination_db_link)
    logging.info("Swapping dbs")
    swap_db(dbinstance, new_rds_DBInstanceIdentifier)
    logging.info(f"Stopping the {dbinstance}-old")
    stop_rds(f"{dbinstance}-old")
    revoke_sgs(from_sg, to_sg, int(port))


def run() -> None:
    log_setup()
    args = parse_arguments()
    if args.db_link:
        migrate_rds(args.db_link)
    else:
        logging.debug("Usage: Requires dbname")


if __name__ == "__main__":
    run()