"""
This script connects to AWS and finds all EBS volumes
that are in the 'available' state (not attached to any EC2 instance).
It then asks the user if they want to delete them.

We are using:
- a *module* (boto3) to talk to AWS
- *functions* to organize the code into reusable blocks
- a *loop* to go through multiple volumes one by one
"""

# -----------------------------
# 1. Import (Modules)
# -----------------------------
# The 'boto3' module lets Python talk to AWS services.
# The 'botocore.exceptions' module helps us handle AWS errors nicely.
import boto3
from botocore.exceptions import ClientError

# -----------------------------
# 2. Configuration section
# -----------------------------
# You can easily change these values below instead of typing them every time.
AWS_REGION = "us-east-1"   # Change this to your AWS region
SIZE_FILTER = 10           # Set to None to show ALL volumes, or a number (GiB) to filter by size
AUTO_DELETE = False         # Change to True if you want to automatically delete matching volumes





# -----------------------------
# 2. Define a function
# -----------------------------
# We use functions so our code is organized and reusable.
# This function lists all available EBS volumes in a specified region. You can change the region as needed.
def list_available_volumes(region=AWS_REGION, size_filter=SIZE_FILTER):
    """
    This function lists all available EBS volumes in the given AWS region.
    """
    # Create an EC2 "client" — like a messenger that talks to AWS EC2
    ec2 = boto3.client("ec2", region_name=region)

    # We'll wrap our AWS call in a 'try/except' to catch possible errors.
    try:
        # Describe all EBS volumes that have status = 'available'
        response = ec2.describe_volumes(
            Filters=[{"Name": "status", "Values": ["available"]}]
        )

        # The AWS response is a dictionary (key-value pairs)
        # The 'Volumes' key holds a list of all volumes found
        volumes = response["Volumes"]

        # If no volumes found, print a friendly message and return (end the function)
        if not volumes:
            print("No available (unattached) EBS volumes found.")
            return []
        
        if size_filter is not None:
            volumes = [v for v in volumes if v["Size"] == size_filter]

            if not volumes:
                print(f"✅ No available EBS volumes found with size {size_filter} GiB.")
                return []

        # Otherwise, print details for each volume
        print(f"Found {len(volumes)} available EBS volume(s):\n")

        # -----------------------------
        # 3. Loops
        # -----------------------------
        # A "loop" is how we repeat a block of code for each item in a list.
        # Here, we use a 'for' loop to go through each volume and print details.
        for vol in volumes:
            print(f"Volume ID: {vol['VolumeId']}")
            print(f"  Size (GiB): {vol['Size']}")
            print(f"  Availability Zone: {vol['AvailabilityZone']}")
            print("-" * 40)

        # Return the list so other functions can use it
        return volumes

    except ClientError as e:
        print("AWS error:", e)
        return []


# -----------------------------
# 4. Another function
# -----------------------------
# This function deletes a list of EBS volumes. Be sure that your region is correct!
def delete_volumes(volumes, region=AWS_REGION):
    """
    Deletes each EBS volume in the given list.
    """
    ec2 = boto3.client("ec2", region_name=region)

    # Use another loop to go through each volume and delete it
    for vol in volumes:
        vol_id = vol["VolumeId"]
        try:
            ec2.delete_volume(VolumeId=vol_id)
            print(f"Deleted volume: {vol_id}")
        except ClientError as e:
            print(f"Could not delete {vol_id}: {e}")


# -----------------------------
# 5. The main program
# -----------------------------
# This part runs when you execute the script directly.
# '__main__' is Python's way of saying "start here".
if __name__ == "__main__":
    print("Checking for available EBS volumes...\n")
    found_volumes = list_available_volumes()

    # If we found any, ask if the user wants to delete them
    if found_volumes:
        answer = input("\nDo you want to delete these volumes? (yes/no): ")
        if answer.lower() == "yes":
            delete_volumes(found_volumes)
            print("\nAll selected volumes deleted.")
        else:
            print("\nNo volumes deleted. Exiting safely.")

