
# Working with EFS

## Launch instances in multiple AZs
1. Create a security group -> security group ID create(input in 3)
aws ec2 create-security-group --group-name SG --description "Temporary SG for the Storage Service Labs"

2. Add a rule for SSH inbound to the security group
aws ec2 authorize-security-group-ingress --group-name SG --protocol tcp --port 22 --cidr 0.0.0.0/0

4. create AMI

5. Launch instance in US-EAST-1A
aws ec2 run-instances --image-id ami-09fdbc3c5aeb77c77 --instance-type t2.micro --placement AvailabilityZone=ap-northeast-1a --security-group-ids sg-052d5c46dc6bdaaf9

4. Launch instance in US-EAST-1B
aws ec2 run-instances --image-id ami-09fdbc3c5aeb77c77 --instance-type t2.micro --placement AvailabilityZone=ap-northeast-1d --security-group-ids sg-052d5c46dc6bdaaf9

## Create an EFS File System

1. Add a rule to the security group to allow the NFS protocol from group members

```
aws ec2 authorize-security-group-ingress --group-id sg-052d5c46dc6bdaaf9 --protocol tcp --port 2049 --source-group sg-052d5c46dc6bdaaf9
```

2. Create an EFS file system through the console, and add the StorageLabs security group to the mount targets for each AZ

## Mount using the NFS Client (perform steps on both instances)
1. Create an EFS mount point
mkdir ~/efs-mount-point
2. Install NFS client
sudo yum -y install nfs-utils
3. Mount using the EFS client
	sudo mount -t nfs4 -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport _EFS-DNS-NAME_:/ ~/efs-mount-point
4. Create a file on the file system
5. Add a file system policy to enforce encryption in-transit
6. Unmount (make sure to change directory out of efs-mount-point first)
	sudo umount ~/efs-mount-point
7. Mount again using the EFS client (what happens?)

## Mount using the EFS utils (perform steps on both instances)
1. Install EFS utils
	sudo yum install -y amazon-efs-utils
2. Mount using the EFS mount helper
sudo mount -t efs -o tls fs-0ac64e961bdc0e0a4.efs.ap-northeast-1.amazonaws.com:/ ~/efs-mount-point

보안 그룹을 설정하여 EFS를 mount하게 되면 해당 보안그룹을 지정한 인스턴스끼리만 통신이 가능하고, mount가능하게 만듬

보안 그룹 소스에 해당 보안그룹이 존재하면, 인바운드 규칙으로 보안그룹에 해당하는 인스턴스만 접근 가능하다는 뜻이다.