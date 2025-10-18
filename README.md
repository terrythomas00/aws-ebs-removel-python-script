# aws-ebs-removel-python-script
# Cleaning Up Unused AWS EBS Volumes

During my time as a Junior DevOps Engineer, one of my responsibilities was helping reduce our AWS costs. To do that, I dug into the monthly billing reports to identify high-cost resources. One major area that stood out was unused EBS (Elastic Block Store) volumes.

**Background**

The AWS environment I worked with was split across multiple VPCs:

**US Region:** prod, staging, beta, dev, and admin

**Canada Region:** prod, staging, and admin

After some investigation, I discovered that:

The **US region** had **over 2,000 available EBS volumes** that weren’t deleted after EC2 instances were terminated.

The **Canada region** had **about 1,500** unused volumes.

These leftover volumes were contributing significantly to monthly storage costs.

# Initial Solution: Bash Script

At the time, I was primarily using Bash. So, I wrote a script to help identify and optionally delete these unused volumes. While it was helpful, it still required some manual review—I would often import or paste a list of volume IDs to double-check the size's before deletion.

Here's the Bash script that listed the EBS volumes and wrote them into a text file that I later used to import using Excel (see below).
```bash
#!/bin/sh
aws ec2 describe-volumes --region us-east-1 --filters Name=status,Values=available,volume-id --output text >> volume2.txt
```

