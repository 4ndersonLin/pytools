import boto3
import json
import sys

policy_name = sys.argv[1]

iam_client = boto3.client('iam')


def get_policy_doc(name):
    try:
        list_rsp = iam_client.list_policies(
            Scope='Local',
            MaxItems=100
        )
    except ClientError as e:
        print('Unexpected error: ' + e)

    policies = list_rsp['Policies']
    target_arn = ''
    target_ver = ''

    for policy in policies:
        if policy['PolicyName'] == name:
            target_arn = policy['Arn']
            target_ver = policy['DefaultVersionId']

    if target_arn == '' and target_ver == '':
        print('No policy: '+policy_name+' in your account.')
        return None
    
    try:
        get_policy_rsp = iam_client.get_policy_version(
            PolicyArn=target_arn,
            VersionId=target_ver
        )
    except ClientError as e:
        print('Unexpected error: ' + e)

    json_policy_doc = json.dumps(get_policy_rsp['PolicyVersion']['Document'], sort_keys=True, indent=4)
    print(json_policy_doc)
    json_f = open(policy_name+'.json', 'w', encoding = 'UTF-8')
    json_f.write(json_policy_doc)
    json_f.close()

def main():
    get_policy_doc(policy_name)

if __name__ == '__main__':
    main()