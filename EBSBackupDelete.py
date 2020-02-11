import boto3
import datetime
import fnmatch
from timeit import default_timer as timer
client = boto3.client('ec2',region_name='Enter Region Here')
snapshots = client.describe_snapshots(OwnerIds=['Enter ID Here'])
start = timer()
x = 0
y = 0
counted = 0
deleted = x - y

for snapshot in snapshots['Snapshots']:
        a=snapshot['StartTime']
        b=a.date()
        c=datetime.datetime.now().date()
        d=c-b
        f=a.day
        string=str(snapshot['Description'])
        pattern=("Created by EBSSnapshotScheduler*")
        match=(fnmatch.fnmatch(string, pattern))
        counted += 1
        
        if d.days>=25 and f!=1 and b!='excludeDate'and match==True:
                try:
                        print(snapshot['SnapshotId'])
                        print('Attempting Deletion')
                        id = snapshot['SnapshotId']
                        client.delete_snapshot(SnapshotId=id)
                        x += 1
                except Exception as e:
                        if 'InvalidSnapshot.InUse' in e.response:
                                print('Snapshot in use, apparently')
                        y += 1
                        print('Deletion Failed')
                        
        else:
            print(snapshot['SnapshotId'])
end = timer()

print('Time taken: ', round(((end - start)/60),4), 'Minutes')
print('Counted: ', counted)
print('Deleted: ', deleted)
